#!/usr/local/bin/python3
#
# Core APRS Client
# Main program
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
import json
from uuid import uuid1
import time
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import base as apbase
import os

import client_shared
from client_utils import (
    get_command_line_params,
    signal_term_handler,
    check_and_create_data_directory,
    client_exception_handler,
    handle_exception,
    check_for_default_config,
)
from client_configuration import load_config, program_config
from client_aprsobject import APRSISObject
from client_message_counter import APRSMessageCounter
from client_expdict import create_expiring_dict, aprs_message_cache
from client_aprs_communication import aprs_callback, init_scheduler_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


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

    # And check if the user still runs with the default config
    # Currently, we do not abort the code but only issue an error to the user
    check_for_default_config()

    # Install our custom exception handler, thus allowing us to signal the
    # user who hosts this bot with a message whenever the program is prone to crash
    # OR has ended. In any case, we will then send the file to the host
    #
    # if you are not interested in a post-mortem call stack, remove the following
    # two lines
    logger.info(msg=f"Activating bot exception handler")
    atexit.register(client_exception_handler)
    sys.excepthook = handle_exception

    # Check whether the data directory exists
    success = check_and_create_data_directory(
        root_path_name=os.path.abspath(os.getcwd()),
        relative_path_name=program_config["data_storage"]["aprs_data_directory"],
    )
    if not success:
        exit(0)

    #
    # Read the message counter
    logger.info(msg="Creating APRS message counter object...")
    client_shared.aprs_message_counter = APRSMessageCounter(
        file_name=program_config["data_storage"]["aprs_message_counter_file_name"]
    )

    # Create the APRS-IS dupe message cache
    client_shared.aprs_message_cache = create_expiring_dict(
        max_len=program_config["dupe_detection"]["msg_cache_max_entries"],
        max_age_seconds=program_config["dupe_detection"]["msg_cache_time_to_live"],
    )

    # Register the SIGTERM handler; this will allow a safe shutdown of the program
    logger.info(msg="Registering SIGTERM handler for safe shutdown...")
    signal.signal(signal.SIGTERM, signal_term_handler)

    # Enter the 'eternal' receive loop
    try:
        while True:
            client_shared.AIS = APRSISObject(
                aprsis_callsign=program_config["client_config"]["aprsis_callsign"],
                aprsis_passwd=str(program_config["network_config"]["aprsis_passcode"]),
                aprsis_host=program_config["network_config"]["aprsis_server_name"],
                aprsis_port=program_config["network_config"]["aprsis_server_port"],
                aprsis_filter=program_config["network_config"]["aprsis_server_filter"],
            )

            # Establish the connection to APRS-IS
            # create a couple of local variables as the 'black' prettifier seems to
            # choke on multi-dimensional dictionaries
            # fmt:off
            _aprsis_server_name = program_config["network_config"]["aprsis_server_name"]
            _aprsis_server_port = str(program_config["network_config"]["aprsis_server_port"])
            _aprsis_server_filter = program_config["network_config"]["aprsis_server_filter"]
            _aprsis_callsign = program_config["client_config"]["aprsis_callsign"]
            _aprsis_passcode = str(program_config["network_config"]["aprsis_passcode"])
            # fmt: on

            logger.info(
                msg=f"Establishing connection to APRS-IS: server={_aprsis_server_name}, port={_aprsis_server_port}, filter={_aprsis_server_filter}, APRS-IS passcode={_aprsis_passcode}, APRS-IS User = {_aprsis_callsign}"
            )
            client_shared.AIS.ais_connect()

            # Are we connected?
            if client_shared.AIS.ais_is_connected():
                logger.debug(msg="Established the connection to APRS-IS")

                # Install the APRS-IS beacon / bulletin schedulers if
                # activated in the program's configuration file
                # Otherwise, this field's value will be 'None'
                aprs_scheduler = init_scheduler_jobs()

                #
                # We are now ready to initiate the actual processing
                # Start the consumer thread
                logger.info(msg="Starting callback consumer")
                client_shared.AIS.ais_start_consumer(aprs_callback)

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
                client_shared.AIS.ais_close()
                client_shared.AIS = None
            else:
                logger.info(msg="Cannot re-establish connection to APRS-IS")

            # Write current number of packets to disk
            logger.info(msg="Writing APRS message counter object to disk ...")
            client_shared.aprs_message_counter.write_counter()

            # Enter sleep mode and then restart the loop
            logger.info(msg=f"Sleeping ...")
            time.sleep(program_config["message_delay"]["packet_delay_message"])

    except (KeyboardInterrupt, SystemExit):
        # Tell the user that we are about to terminate our work
        logger.info(
            msg="KeyboardInterrupt or SystemExit in progress; shutting down ..."
        )

        # write most recent APRS message counter to disk
        logger.info(msg="Writing APRS message counter object to disk ...")
        client_shared.aprs_message_counter.write_counter()

        if aprs_scheduler:
            logger.info(msg="Pausing aprs_scheduler")
            aprs_scheduler.pause()
            aprs_scheduler.remove_all_jobs()
            logger.info(msg="Shutting down aprs_scheduler")
            if aprs_scheduler.state != apbase.STATE_STOPPED:
                try:
                    aprs_scheduler.shutdown()
                except:
                    logger.info(
                        msg="Exception during scheduler shutdown SystemExit loop"
                    )

        # Close APRS-IS connection whereas still present
        if client_shared.AIS.ais_is_connected():
            logger.info(msg="Closing connection to APRS-IS")
            client_shared.AIS.ais_close()


if __name__ == "__main__":
    run_listener()
