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
    make_pretty_aprs_messages,
    parse_bulletin_data,
    client_exception_handler,
    handle_exception,
    check_for_default_config,
)
from client_configuration import load_config, program_config
from input_parser import parse_input_message
from output_generator import generate_output_message
from _version import __version__

from client_message_counter import (
    read_aprs_message_counter,
    write_aprs_message_counter,
    aprs_message_counter,
)

from client_expdict import create_expiring_dict,aprs_message_cache

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
from apscheduler.schedulers import base as apbase
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# APRSlib callback
# Extract the fields from the APRS message, start the parsing process,
# execute the command and send the command output back to the user
def aprs_callback(raw_aprs_packet: dict):
    """
    aprslib callback; this is the core process that takes care of everything
    Parameters
    ==========
    raw_aprs_packet: 'dict'
        dict object, containing the raw APRS data
    Returns
    =======
    """
    global aprs_message_counter
    global aprs_message_cache
    global AIS

    # Get our relevant fields from the APRS message
    addresse_string = raw_aprs_packet.get("addresse")
    message_text_string = raw_aprs_packet.get("message_text")
    response_string = raw_aprs_packet.get("response")
    msgno_string = raw_aprs_packet.get("msgNo")
    from_callsign = raw_aprs_packet.get("from")
    format_string = raw_aprs_packet.get("format")
    ackMsgno_string = raw_aprs_packet.get("ackMsgNo")

    # lower the response in case we received one
    if response_string:
        response_string = response_string.lower()

    # Check if we need to deal with the old vs the new message format
    new_ackrej_format = True if ackMsgno_string else False

    # Check if this request supports a msgno
    msg_no_supported = True if msgno_string else False

    # User's call sign. read: who has sent us this message?
    if from_callsign:
        from_callsign = from_callsign.upper()

    if addresse_string:
        # Lets examine what we've got:
        # 1. Message format should always be 'message'.
        #    This is even valid for ack/rej responses
        # 2. Message text should contain content
        # 3. response text should NOT be ack/rej
        # Continue if both assumptions are correct
        if (
            format_string == "message"
            and message_text_string
            and response_string not in ["ack", "rej"]
        ):
            # This is a message that belongs to us

            # logger.info(msg=dump_string_to_hex(message_text_string))

            # Check if the message is present in our decaying message cache
            # If the message can be located, then we can assume that we have
            # processed (and potentially acknowledged) that message request
            # within the last e.g. 5 minutes and that this is a delayed / dupe
            # request, thus allowing us to ignore this request.
            aprs_message_key = get_aprs_message_from_cache(
                message_text=message_text_string,
                message_no=msgno_string,
                users_callsign=from_callsign,
                aprs_cache=aprs_message_cache,
            )
            if aprs_message_key:
                logger.debug(
                    msg="DUPLICATE APRS PACKET - this message is still in our decaying message cache"
                )
                logger.debug(
                    msg=f"Ignoring duplicate APRS packet raw_aprs_packet: {raw_aprs_packet}"
                )
            else:
                logger.debug(msg=f"Received raw_aprs_packet: {raw_aprs_packet}")

                # Send an ack if we DID receive a message number
                # and we DID NOT have received a request in the
                # new ack/rej format
                # see aprs101.pdf pg. 71ff.
                if msg_no_supported and not new_ackrej_format:
                    send_ack(
                        myaprsis=AIS,
                        simulate_send=program_config["testing"]["aprsis_simulate_send"],
                        alias=program_config["client_config"]["aprsis_callsign"],
                        tocall=program_config["client_config"]["aprsis_tocall"],
                        users_callsign=from_callsign,
                        source_msg_no=msgno_string,
                        packet_delay=program_config["message_delay"][
                            "packet_delay_ack"
                        ],
                    )
                #
                # This is where the magic happens: Try to figure out what the user
                # wants from us. If we were able to understand the user's message,
                # 'success' will be true. In any case, the 'response_parameters'
                # dictionary will give us a hint about what to do next (and even
                # contains the parser's error message if 'success' != True)
                # input parameters: the actual message, the user's call sign and
                # the aprs.fi API access key for location lookups
                success, response_parameters = parse_input_message(
                    aprs_message=message_text_string,
                    from_callsign=from_callsign,
                )
                logger.info(msg=f"Input parser result: {success}")
                logger.info(msg=response_parameters)
                #
                # If the 'success' parameter is True, then we should know
                # by now what the user wants from us. Now, we'll leave it to
                # another module to generate the output data of what we want
                # to send to the user.
                # The result to this post-processor will be a general success
                # status code and a list item, containing the messages that are
                # ready to be sent to the user.
                #
                # parsing successful?
                if success:
                    # Generate the output message for the requested keyword
                    # The 'success' status is ALWAYS positive even if the
                    # message could not get processed - the inline'd error
                    # message counts as positive message content
                    success, output_message = generate_output_message(
                        response_parameters=response_parameters,
                    )
                # darn - we failed to hail the Tripods
                # this is the branch where the input parser failed to understand
                # the message. A possible reason: you sent a keyword which requires
                # an additional parameter but failed to send that one, too.
                # As we only parse but never process data in that input
                # parser, we sinply don't know what to do with the user's message
                # and get back to him with a generic response.
                else:
                    input_parser_error_message = response_parameters[
                        "input_parser_error_message"
                    ]
                    # Dump the human readable message to the user if we have one
                    if input_parser_error_message:
                        output_message = make_pretty_aprs_messages(
                            message_to_add=f"{input_parser_error_message}",
                            add_sep=False,
                        )
                    # If not, just dump the link to the instructions
                    # This is the default branch which dumps generic information
                    # to the client whenever there is no generic error text from the input parser
                    else:
                        output_message = make_pretty_aprs_messages(
                            message_to_add="Sorry, did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client",
                            add_sep=False,
                        )
                        logger.info(
                            msg=f"Unable to process APRS packet {raw_aprs_packet}"
                        )

                # Send our message(s) to APRS-IS
                aprs_message_counter.value = send_aprs_message_list(
                    myaprsis=AIS,
                    simulate_send=program_config["testing"]["aprsis_simulate_send"],
                    message_text_array=output_message,
                    destination_call_sign=from_callsign,
                    send_with_msg_no=msg_no_supported,
                    aprs_message_counter=aprs_message_counter.value,
                    external_message_number=msgno_string,
                    new_ackrej_format=new_ackrej_format,
                )

                # We've finished processing this message. Update the decaying
                # cache with our message.
                # Store the core message data in our decaying APRS message cache
                # Dupe detection is applied regardless of the message's
                # processing status
                aprs_message_cache = add_aprs_message_to_cache(
                    message_text=message_text_string,
                    message_no=msgno_string,
                    users_callsign=from_callsign,
                    aprs_cache=aprs_message_cache,
                )


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

    global aprs_message_counter
    global aprs_message_cache
    global AIS

    # init our (future) global variables
    apscheduler = AIS = None

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
    logger.info(msg="Reading APRS message counter...")
    aprs_message_counter = read_aprs_message_counter(
        file_name=program_config["data_storage"]["aprs_message_counter_file_name"]
    )

    # Initialize the aprs-is object
    AIS = None

    aprs_message_cache= create_expiring_dict(max_len=program_config["dupe_detection"]["msg_cache_max_entries"],max_age_seconds=program_config["dupe_detection"]["msg_cache_time_to_live"])

    """
    # Create some local variables as otherwise, the 'black' prettifier will choke on it
    _msg_cache_max_entries = program_config["dupe_detection"]["msg_cache_max_entries"]
    _msg_cache_time_to_live = program_config["dupe_detection"]["msg_cache_time_to_live"]

    # Create the decaying APRS message cache. Any APRS message that is present in
    # this cache will be considered as a duplicate / delayed and will not be processed
    message = f"APRS message dupe cache set to {str(_msg_cache_max_entries)}  max possible entries and a TTL of {str(_msg_cache_time_to_live / 60)} mins"

    logger.info(msg=message)
    aprs_message_cache = ExpiringDict(
        max_len=program_config["dupe_detection"]["msg_cache_max_entries"],
        max_age_seconds=program_config["dupe_detection"]["msg_cache_time_to_live"],
    )
    """

    # Register the SIGTERM handler; this will allow a safe shutdown of the program
    logger.info(msg="Registering SIGTERM handler for safe shutdown...")
    signal.signal(signal.SIGTERM, signal_term_handler)

    # Enter the 'eternal' receive loop
    try:
        while True:
            # Create the APRS-IS object and set user/pass/host/port
            AIS = aprslib.IS(
                callsign=program_config["client_config"]["aprsis_callsign"],
                passwd=str(program_config["network_config"]["aprsis_passcode"]),
                host=program_config["network_config"]["aprsis_server_name"],
                port=program_config["network_config"]["aprsis_server_port"],
            )

            # Set the APRS-IS server filter
            AIS.set_filter(program_config["network_config"]["aprsis_server_filter"])

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
                        # Example nessage: COAC>APRS:=5150.34N/00819.60E?COAC 0.01
                        # results in
                        # lat = 5150.34N
                        # primary symbol identifier = /
                        # lon = 00819.60E
                        # symbol identifier = ?
                        # plus some text.
                        # The overall total symbol code /? refers to a server icon - see list of symbols
                        #
                        # as all of our parameters are stored in a dictionary, we need to construct

                        # create a couple of local variables as the 'black' prettifier seems to
                        # choke on multi-dimensional dictionaries

                        # fmt:off
                        _aprsis_latitude = program_config["beacon_config"]["aprsis_latitude"]
                        _aprsis_longitude = program_config["beacon_config"]["aprsis_longitude"]
                        _aprsis_table = program_config["beacon_config"]["aprsis_table"]
                        _aprsis_symbol = program_config["beacon_config"]["aprsis_symbol"]
                        _aprsis_callsign = program_config["client_config"]["aprsis_callsign"]
                        _aprsis_beacon_altitude_ft = str(program_config["beacon_config"]["aprsis_beacon_altitude_ft"])[:6]
                        # fmt:on

                        # generate our beacon string
                        _beacon = f"{_aprsis_latitude}{_aprsis_table}{_aprsis_longitude}{_aprsis_symbol}{_aprsis_callsign} {__version__} /A={_aprsis_beacon_altitude_ft}"

                        # and store it in a list item
                        aprs_beacon_messages: list = [_beacon]

                        # Ultimately, send the beacon
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
                        aprs_bulletin_messages = parse_bulletin_data(
                            core_config=program_config
                        )

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
                AIS.consumer(aprs_callback, blocking=True, immortal=True, raw=False)

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
            write_aprs_message_counter(
                file_name=program_config["data_storage"][
                    "aprs_message_counter_file_name"
                ],
            )

            # Enter sleep mode and then restart the loop
            logger.info(msg=f"Sleeping ...")
            time.sleep(program_config["message_delay"]["packet_delay_message"])

    except (KeyboardInterrupt, SystemExit):
        # Tell the user that we are about to terminate our work
        logger.info(
            msg="KeyboardInterrupt or SystemExit in progress; shutting down ..."
        )

        # write most recent APRS message counter to disk
        logger.info(msg="Writing APRS message counter to disk ...")
        write_aprs_message_counter(
            file_name=program_config["data_storage"]["aprs_message_counter_file_name"],
        )

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
        if AIS:
            logger.info(msg="Closing connection to APRS-IS")
            AIS.close()


if __name__ == "__main__":
    run_listener()
