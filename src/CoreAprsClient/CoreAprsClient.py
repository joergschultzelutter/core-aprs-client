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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import signal
import time
import atexit
import os
from functools import partial
import logging
from pprint import pformat
from collections.abc import Callable
from typing import Dict, Any, Mapping
import threading
import copy
from types import MappingProxyType

from . import client_shared
from .client_utils import (
    signal_term_handler,
    check_and_create_data_directory,
    client_exception_handler,
    handle_exception,
    check_for_default_config,
    finalize_pretty_aprs_messages,
    make_pretty_aprs_messages,
)
from .client_configuration import load_config, program_config
from .client_aprsobject import APRSISObject
from .client_message_counter import APRSMessageCounter
from .client_expdict import create_expiring_dict
from .client_aprs_communication import (
    aprs_callback,
    init_scheduler_jobs,
    remove_scheduler,
)
from .client_logger import logger, update_logging_level
from .client_return_codes import CoreAprsClientInputParserStatus


class CoreAprsClient:
    config_file: str
    log_level: int
    input_parser: Callable[..., Any]
    output_generator: Callable[..., Any]

    def __init__(
        self,
        config_file: str,
        input_parser: Callable[..., Any],
        output_generator: Callable[..., Any],
        log_level: int = logging.INFO,
    ):
        self.config_file = config_file
        self.input_parser = input_parser
        self.output_generator = output_generator
        self.log_level = log_level
        self._dynamic_aprs_bulletins: Dict[str, Any] = {}
        self._lock = threading.Lock()

        # Prepare the config file handler
        # Check if the config file exists
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found")

        # load the program config from our external config file
        load_config(config_file=self.config_file)
        if len(program_config) == 0:
            logger.error(
                msg="Program config file is empty or contains an error; exiting"
            )
            sys.exit(0)

        # And check if the user still runs with the default config
        # Currently, we do not abort the code but only issue an error to the user
        check_for_default_config()

        # Finally, create the MappingProxyType copy of the configuration
        # so that we can expose it to the user, if requested.
        self._config_data = MappingProxyType(program_config.copy())

        # Update the log level (if needed)
        update_logging_level(logging_level=self.log_level)

    def activate_client(self):
        """
        This function is responsible for setting up the communication
        with APRS-IS. It reads the configuration file and establishes
        the network communication with the APRS-IS server. Finally, the
        aprslib's callback function gets triggered.

        Parameters
        ==========

        Returns
        =======

        """

        # Install our custom exception handler, thus allowing us to signal the
        # user who hosts this bot with a message whenever the program is prone to crash
        # OR has ended. In any case, we will then send the file to the host
        #
        # if you are not interested in a post-mortem call stack, remove the following
        # two lines
        logger.debug(msg=f"Activating bot exception handler")
        atexit.register(client_exception_handler)
        sys.excepthook = handle_exception

        # Check whether the data directory exists
        success = check_and_create_data_directory(
            root_path_name=os.path.abspath(os.getcwd()),
            relative_path_name=program_config["coac_data_storage"][
                "aprs_data_directory"
            ],
        )
        if not success:
            exit(0)

        #
        # Read the message counter
        client_shared.aprs_message_counter = APRSMessageCounter(
            file_name=program_config["coac_data_storage"][
                "aprs_message_counter_file_name"
            ]
        )

        # Create the APRS-IS dupe message cache
        client_shared.aprs_message_cache = create_expiring_dict(
            max_len=program_config["coac_dupe_detection"]["msg_cache_max_entries"],
            max_age_seconds=program_config["coac_dupe_detection"][
                "msg_cache_time_to_live"
            ],
        )

        # Register the SIGTERM handler; this will allow a safe shutdown of the program
        logger.debug(msg="Registering SIGTERM handler for safe shutdown...")
        signal.signal(signal.SIGTERM, signal_term_handler)

        # Create the future aprs_scheduler variable
        aprs_scheduler = None

        # Enter the 'eternal' receive loop
        try:
            while True:
                client_shared.AIS = APRSISObject(
                    aprsis_callsign=program_config["coac_client_config"][
                        "aprsis_callsign"
                    ],
                    aprsis_passwd=str(
                        program_config["coac_network_config"]["aprsis_passcode"]
                    ),
                    aprsis_host=program_config["coac_network_config"][
                        "aprsis_server_name"
                    ],
                    aprsis_port=program_config["coac_network_config"][
                        "aprsis_server_port"
                    ],
                    aprsis_filter=program_config["coac_network_config"][
                        "aprsis_server_filter"
                    ],
                )

                # Connect to APRS-IS
                logger.debug(msg="Establishing connection to APRS-IS...")
                client_shared.AIS.ais_connect()

                # Are we connected?
                if client_shared.AIS.ais_is_connected():
                    logger.debug(msg="Established the connection to APRS-IS")

                    # Install the APRS-IS beacon / bulletin schedulers if
                    # activated in the program's configuration file
                    # Otherwise, this field's value will be 'None'
                    aprs_scheduler = init_scheduler_jobs(class_instance=self)

                    # create the partial object for our callback
                    enhanced_callback = partial(
                        aprs_callback,
                        parser=self.input_parser,
                        generator=self.output_generator,
                    )

                    #
                    # We are now ready to initiate the actual processing
                    # Start the consumer thread
                    logger.info(msg="Starting APRS-IS callback consumer")
                    client_shared.AIS.ais_start_consumer(enhanced_callback)

                    #
                    # We have left the callback, let's clean up a few things
                    logger.debug(msg="Have left the callback consumer")
                    #
                    # First, stop all schedulers. Then remove the associated jobs
                    # This will prevent the beacon/bulletin processes from sending out
                    # messages to APRS_IS
                    # Note that the scheduler might not be active - its existence depends
                    # on the user's configuration file settings.
                    if aprs_scheduler:
                        remove_scheduler(aprs_scheduler=aprs_scheduler)
                    aprs_scheduler = None

                    # close the connection to APRS-IS
                    logger.debug(msg="Closing APRS connection to APRS-IS")
                    client_shared.AIS.ais_close()
                    client_shared.AIS = None
                else:
                    logger.debug(msg="Cannot re-establish connection to APRS-IS")

                # Write current number of packets to disk
                client_shared.aprs_message_counter.write_counter()

                # Enter sleep mode and then restart the loop
                logger.debug(msg=f"Sleeping ...")
                time.sleep(program_config["coac_message_delay"]["packet_delay_message"])

        except (KeyboardInterrupt, SystemExit):
            # Tell the user that we are about to terminate our work
            logger.debug(
                msg="KeyboardInterrupt or SystemExit in progress; shutting down ..."
            )

            # write most recent APRS message counter to disk
            client_shared.aprs_message_counter.write_counter()

            # Shutdown (and remove) the scheduler if it still exists
            if aprs_scheduler:
                remove_scheduler(aprs_scheduler=aprs_scheduler)

            # Close APRS-IS connection whereas still present
            if client_shared.AIS.ais_is_connected():
                client_shared.AIS.ais_close()

    def dryrun_testcall(self, message_text: str, from_callsign: str):
        """
        This function can be used for 100% offline testing. It does trigger
        the standard input parser and output generator.

        Parameters
        ==========
        message_text: str
            The (simulated) APRS input message; sent to us by "from_callsign"
        from_callsign: str
            The callsign that the message was sent from

        Returns
        =======
        none
        """
        logger.info("Activating dryrun testcall...")

        # load the program config from our external config file
        load_config(config_file=self.config_file)
        if len(program_config) == 0:
            logger.error(
                msg="Program config file is empty or contains an error; exiting"
            )
            sys.exit(0)

        # Register the on_exit function to be called on program exit
        atexit.register(client_exception_handler)

        # Set up the exception handler to catch unhandled exceptions
        sys.excepthook = handle_exception

        logger.info(
            msg=f"parsing message '{message_text}' for callsign '{from_callsign}'"
        )

        retcode, input_parser_error_message, response_parameters = self.input_parser(
            aprs_message=message_text, from_callsign=from_callsign
        )

        logger.info(msg="Parsed message:")
        logger.info(msg=pformat(response_parameters))
        logger.info(msg=f"return code: {retcode}")
        match retcode:
            case CoreAprsClientInputParserStatus.PARSE_OK:

                logger.info("Running Output Processor build ...")

                # (Try to) build the outgoing message string
                success, output_message_string = self.output_generator(
                    input_parser_response_object=response_parameters
                )
                logger.info(msg=f"Output Processor response={success}, message:")
                logger.info(msg=output_message_string)

                # Generate the outgoing content, if successful
                if success:
                    logger.info(
                        "Output processor status successful; building outgoing messages ..."
                    )
                    # Convert to pretty APRS messaging
                    output_message = make_pretty_aprs_messages(
                        message_to_add=output_message_string
                    )

                    # And finalize the output message, if needed
                    output_message = finalize_pretty_aprs_messages(
                        mylistarray=output_message
                    )
                else:
                    logger.info("Output processor status unsuccessful")
                    # This code branch should never be reached unless there is a
                    # discrepancy between the action determined by the input parser
                    # and the responsive counter-action in the output processor
                    output_message = make_pretty_aprs_messages(
                        message_to_add=program_config["coac_client_config"][
                            "aprs_input_parser_default_error_message"
                        ],
                    )
                logger.info(msg=pformat(output_message))
            case CoreAprsClientInputParserStatus.PARSE_ERROR | _:
                logger.error(
                    msg="input_parser_error_message = {input_parser_error_message}"
                )
                # Dump the human readable message to the user if we have one
                if input_parser_error_message:
                    output_message = make_pretty_aprs_messages(
                        message_to_add=f"{input_parser_error_message}",
                    )
                # If not, just dump the link to the instructions
                else:
                    output_message = make_pretty_aprs_messages(
                        message_to_add=program_config["coac_client_config"][
                            "aprs_input_parser_default_error_message"
                        ],
                    )
                # Ultimately, finalize the outgoing message(s) and add the message
                # numbers if the user has requested this in his configuration
                # settings
                output_message = finalize_pretty_aprs_messages(
                    mylistarray=output_message
                )

                logger.info(pformat(output_message))
                logger.info(msg=pformat(response_parameters))

    @property
    def dynamic_aprs_bulletins(self) -> Mapping[str, Any]:
        with self._lock:
            return MappingProxyType(self._dynamic_aprs_bulletins)

    @dynamic_aprs_bulletins.setter
    def dynamic_aprs_bulletins(self, new_dict: Dict[str, Any]) -> None:
        with self._lock:
            self._dynamic_aprs_bulletins = copy.deepcopy(new_dict)

    @property
    def config_data(self) -> Mapping[str, Any]:
        with self._lock:
            return self._config_data
