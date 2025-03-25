#!/usr/local/bin/python3
#
# Core APRS Client
# Author: Joerg Schultze-Lutter, 2025
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
import sys
import signal
import logging
import aprslib
from expiringdict import ExpiringDict
from utils import (
    add_aprs_message_to_cache,
    get_aprs_message_from_cache,
    get_command_line_params,
    signal_term_handler,
    check_if_file_exists,
    check_and_create_data_directory,
    create_zip_file_from_log,
    send_apprise_message,
    read_aprs_message_counter,
    write_aprs_message_counter,
    make_pretty_aprs_messages,
    parse_bulletin_data,
    client_exception_handler,
    handle_exception,
)
from client_configuration import load_config, program_config
from input_parser import parse_input_message
from output_generator import generate_output_message
from _version import __version__

import json
from uuid import uuid1
from aprs_communication import (
    send_ack,
    send_aprs_message_list,
    send_bulletin_messages,
    send_beacon_and_status_msg,
)
import time
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# init our (future) global variables
apscheduler = AIS = aprs_message_cache = aprs_message_conter = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# These are global variables which will be used
# in case of an uncaught exception where we send
# the host a final Apprise message along with the
# program's stack trace
exception_occurred = False
ex_type = ex_value = ex_traceback = None

#
# The program's bulletin message (optional)
# This dictionary receives its data from the program's configuration file
#
aprs_bulletin_messages: dict = {}


def run_listener():
    """
    Main listener
    Establishes a listener to APRS-IS and activates APRS callback

    Parameters
    ==========

    Returns
    =======

    """
    logger.info(msg="Startup ....")

    # Get the command line params
    configfile = get_command_line_params()

    if not configfile:
        sys.exit(0)

    # load the program config from our external config file
    load_config(config_file=configfile)
    if len(program_config) == 0:
        logger.info(msg="Program config file is empty or contains an error; exiting")
        sys.exit(0)

    if program_config["client_config"]["aprsis_tocall"] == "APRS":
        logger.error(
            msg="'aprsis_tocall' is still set to default config; change config file ASAP"
        )

    if program_config["client_config"]["aprsis_callsign"] == "COAC":
        logger.error(
            msg="'aprsis_callsign' is still set to default config; change config file ASAP"
        )

    # Install our custom exception handler, thus allowing us to signal the
    # user who hosts MPAD with a message whenever the program is prone to crash
    # OR has ended. In any case, we will then send the file to the host
    #
    # if you are not interested in a post-mortem call stack, remove the following
    # two lines
    logger.info(msg=f"Activating MPAD exception handler")
    atexit.register(client_exception_handler)
    sys.excepthook = handle_exception

    # Check whether the data directory exists
    success = check_and_create_data_directory()
    if not success:
        exit(0)

    #
    # Read the message counter (function will create the S3 object if it does not exist in the bucket)
    logger.info(msg="Reading APRS message counter...")
    aprs_message_counter = read_aprs_message_counter()

    # Initialize the aprs-is object
    AIS = None

    # Create the decaying APRS message cache. Any APRS message that is present in
    # this cache will be considered as a duplicate / delayed and will not be processed
    message = (
        "APRS message dupe cache set to "
        + program_config["dupe_detection"]["msg_cache_max_entries"]
        + " max possible entries and a TTL of "
        + (program_config["dupe_detection"]["msg_cache_time_to_live"] / 60)
        + " mins"
    )

    logger.info(msg=message)
    aprs_message_cache = ExpiringDict(
        max_len=program_config["dupe_detection"]["msg_cache_max_entries"],
        max_age_seconds=program_config["dupe_detection"]["msg_cache_time_to_live"],
    )

    # Register the SIGTERM handler; this will allow a safe shutdown of the program
    logger.info(msg="Registering SIGTERM handler for safe shutdown...")
    signal.signal(signal.SIGTERM, signal_term_handler)

    # Enter the 'eternal' receive loop
    try:
        while True:
            # Create the APRS-IS object and set user/pass/host/port
            AIS = aprslib.IS(
                callsign=program_config["client_config"]["aprsis_callsign"],
                passwd=program_config["network_config"]["aprsis_passcode"],
                host=program_config["network_config"]["aprsis_server_name"],
                port=program_config["network_config"]["aprsis_server_port"],
            )

            # Set the APRS-IS server filter
            AIS.set_filter(program_config["network_config"]["aprsis_server_filter"])

            # Establish the connection to APRS-IS
            message = (
                "Establishing connection to APRS-IS: server="
                + program_config["network_config"]["aprsis_server_name"]
                + ", port="
                + str(program_config["network_config"]["aprsis_server_port"])
                + ", filter="
                + program_config["network_config"]["aprsis_server_filter"]
                + ", APRS-IS User:"
                + program_config["network_client_config"]["aprsis_callsign"]
                + ", APRS-IS passcode:"
                + str(program_config["network_config"]["aprsis_passcode"])
            )
            logger.info(msg=message)
            logger.info(msg="Establishing connection to APRS-IS")
            AIS.connect(blocking=True)

            # Are we connected?
            if AIS._connected:
                logger.debug(msg="Established the connection to APRS-IS")

                aprs_scheduler = None
                if (
                    program_config["beacon_config"]["aprsis_broadcast_beacon"]
                    or program_config["bulletin_config"]["aprsis_broadcast_bulletins"]
                ):
                    # If we reach this position in the code, we have at least one
                    # task that needs to be scheduled (bulletins and/or position messages
                    #
                    # Create the scheduler
                    aprs_scheduler = BackgroundScheduler()

                    # Install two schedulers tasks, if requested by the user
                    # The first task is responsible for sending out beacon messages
                    # to APRS; it will be triggered every 30 mins
                    #

                    # The 2nd task is responsible for sending out bulletin messages
                    # to APRS; it will be triggered every 4 hours
                    #

                    if program_config["beacon_config"]["aprsis_broadcast_beacon"]:
                        # Send initial beacon after establishing the connection to APRS_IS
                        logger.info(
                            msg="Send initial beacon after establishing the connection to APRS_IS"
                        )

                        #
                        # APRS_IS beacon messages (will be sent every 30 mins)
                        # - APRS Position (first line) needs to have 63 characters or less
                        # - APRS Status can have 67 chars (as usual)
                        # Details: see aprs101.pdf chapter 8
                        #
                        # The client will NOT check the content and send it out 'as is'
                        #
                        # This message is a position report; format description can be found on pg. 23ff and pg. 94ff.
                        # of aprs101.pdf. Message symbols: see http://www.aprs.org/symbols/symbolsX.txt and aprs101.pdf
                        # on page 104ff.
                        # Format is as follows: =Lat primary-symbol-table-identifier lon symbol-identifier test-message
                        # Lat/lon from the configuration have to be valid or the message will not be accepted by aprs-is
                        #
                        # Example nessage: MPAD>APRS:=5150.34N/00819.60E?COAC 0.01
                        # results in
                        # lat = 5150.34N
                        # primary symbol identifier = /
                        # lon = 00819.60E
                        # symbol identifier = ?
                        # plus some text.
                        # The overall total symbol code /? refers to a server icon - see list of symbols
                        #
                        # as all of our parameters are stored in a dictionary, we need to construct

                        _beacon = (
                            program_config["beacon_config"]["aprsis_latitude"]
                            + program_config["beacon_config"]["aprsis_table"]
                            + program_config["beacon_config"]["aprsis_longitude"]
                            + program_config["beacon_config"]["aprsis_symbol"]
                            + program_config["client_config"]["aprsis_callsign"]
                            + " "
                            + __version__
                            + " /A="
                            + str(
                                program_config["beacon_config"][
                                    "aprsis_beacon_altitude_ft"
                                ]
                            )[:6]
                        )
                        aprs_beacon_messages: list = [_beacon]
                        #

                        send_beacon_and_status_msg(
                            myaprsis=AIS,
                            aprs_beacon_messages=aprs_beacon_messages,
                            simulate_send=program_config["testing"][
                                "aprsis_simulate_send"
                            ],
                        )

                        # Add position beaconing to scheduler
                        aprs_scheduler.add_job(
                            send_beacon_and_status_msg,
                            "interval",
                            id="aprsbeacon",
                            minutes=program_config["beacon_config"][
                                "aprsis_beacon_interval_minutes"
                            ],
                            args=[
                                AIS,
                                aprs_beacon_messages,
                                program_config["testing"]["aprsis_simulate_send"],
                            ],
                        )

                    if program_config["bulletin_config"]["aprsis_broadcast_bulletins"]:
                        # prepare the bulletin data
                        parse_bulletin_data(core_config=program_config)

                        # Install scheduler task 2 - send standard bulletins (advertising the program instance)
                        # The bulletin messages consist of fixed content and are defined at the beginning of
                        # this program code
                        aprs_scheduler.add_job(
                            send_bulletin_messages,
                            "interval",
                            id="aprsbulletin",
                            minutes=program_config["bulletin_config"][
                                "aprsis_bulletin_interval_minutes"
                            ],
                            args=[
                                AIS,
                                aprs_bulletin_messages,
                                program_config["testing"]["aprsis_simulate_send"],
                            ],
                        )

                    # Ultimately, start the scheduler
                    aprs_scheduler.start()

                #
                # We are now ready to initiate the actual processing
                # Start the consumer thread
                logger.info(msg="Starting callback consumer")
                AIS.consumer(mycallback, blocking=True, immortal=True, raw=False)

                #
                # We have left the callback, let's clean up a few things
                logger.info(msg="Have left the callback consumer")
                #
                # First, stop all schedulers. Then remove the associated jobs
                # This will prevent the beacon/bulletin processes from sending out
                # messages to APRS_IS
                # Note that the scheduler might not be active - its existence depends
                # on the user's configuration file settings.
                if aprs_scheduler:
                    # pause the scheduler and remove all jobs
                    aprs_scheduler.pause()
                    aprs_scheduler.remove_all_jobs()
                    if (
                        aprs_scheduler.state
                        != apscheduler.schedulers.base.STATE_STOPPED
                    ):
                        try:
                            aprs_scheduler.shutdown()
                        except:
                            logger.info(
                                msg="Exception during scheduler shutdown eternal loop"
                            )

                #
                # close connection
                logger.debug(msg="Closing APRS connection to APRS-IS")
                AIS.close()
                AIS = None
            else:
                logger.info(msg="Cannot re-establish connection to APRS-IS")
            write_aprs_message_counter(aprs_message_counter=aprs_message_counter)

            # Enter sleep mode and then restart the loop
            logger.info(msg=f"Sleeping ...")
            time.sleep(program_config["message_delay"]["packet_delay_message"])

    except (KeyboardInterrupt, SystemExit):
        # Tell the user that we are about to terminate our work
        logger.info(
            msg="KeyboardInterrupt or SystemExit in progress; shutting down ..."
        )

        # write most recent APRS message counter to disc
        logger.info(msg="Writing APRS message counter to disc ...")
        write_aprs_message_counter(aprs_message_counter=aprs_message_counter)

        if aprs_scheduler:
            logger.info(msg="Pausing aprs_scheduler")
            aprs_scheduler.pause()
            aprs_scheduler.remove_all_jobs()
            logger.info(msg="Shutting down aprs_scheduler")
            if aprs_scheduler.state != apscheduler.schedulers.base.STATE_STOPPED:
                try:
                    aprs_scheduler.shutdown()
                except:
                    logger.info(
                        msg="Exception during scheduler shutdown SystemExit loop"
                    )

        # Close APRS-IS connection whereas still present
        if AIS:
            logger.info(msg="Closing connection to APRS-IS")
            AIS.close()


if __name__ == "__main__":
    run_listener()
