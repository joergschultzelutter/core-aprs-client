#!/usr/local/bin/python3
#
# Core APRS Client
# Input / Output stub testing
# Author: Joerg Schultze-Lutter, 2025
#
# This program can be used for a 100% offline simulation
# and uses the framework's both input parser and output generator
#
# Pass both callsign and APRS message to this program's 'testcall'
# method - which will then trigger the input parser and output generator
# You will receive exactly the same results as with the 'live client' - but
# no content will be received from / sent to APRS-IS
#
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
from client_utils import (
    make_pretty_aprs_messages,
    client_exception_handler,
    handle_exception,
    get_command_line_params,
    finalize_pretty_aprs_messages,
)
from client_input_parser import parse_input_message
from client_output_generator import generate_output_message
from pprint import pformat
import sys
import atexit
from client_configuration import load_config, program_config
from client_logger import logger

exception_occurred = False
ex_type = ex_value = ex_traceback = None


def testcall(message_text: str, from_callsign: str):
    """
    Simulates an external call from APRS-IS. You can use this
    function for integration testing. It performs the same
    steps as core-aprs-client's live routines - but everything
    happens 100% offline and there is no communication between
    the program and APRS-IS.

    Parameters
    ==========
    message_text: 'str'
       The incoming APRS message. 1..67 bytes in length
    from_callsign: 'str'
       The sender's call sign

    Returns
    =======
    """
    # Get the command line params
    configfile = get_command_line_params()
    if not configfile:
        sys.exit(0)

    # load the program config from our external config file
    load_config(config_file=configfile)
    if len(program_config) == 0:
        logger.error(msg="Program config file is empty or contains an error; exiting")
        sys.exit(0)

    # Register the on_exit function to be called on program exit
    atexit.register(client_exception_handler)

    # Set up the exception handler to catch unhandled exceptions
    sys.excepthook = handle_exception

    logger.info(msg=f"parsing message '{message_text}' for callsign '{from_callsign}'")

    success, response_parameters = parse_input_message(
        aprs_message=message_text, from_callsign=from_callsign
    )

    logger.info(msg=pformat(response_parameters))
    logger.info(msg=f"success: {success}")
    if success:
        # enrich our response parameters with all API keys that we need for
        # the completion of the remaining tasks. The APRS access details
        # are not known and will be set to simulation mode
        logger.info(msg="Response:")
        output_message = generate_output_message(response_parameters)
        output_message = finalize_pretty_aprs_messages(mylistarray=output_message)
        logger.info(msg=pformat(output_message))
    else:
        input_parser_error_message = response_parameters["input_parser_error_message"]
        # Dump the HRM to the user if we have one
        if input_parser_error_message:
            output_message = make_pretty_aprs_messages(
                message_to_add=f"{input_parser_error_message}",
            )
        # If not, just dump the link to the instructions
        else:
            output_message = make_pretty_aprs_messages(
                message_to_add=program_config["client_config"][
                    "aprs_input_parser_default_error_message"
                ],
            )
        # Ultimately, finalize the outgoing message(s) and add the message
        # numbers if the user has requested this in his configuration
        # settings
        output_message = finalize_pretty_aprs_messages(mylistarray=output_message)

        logger.info(pformat(output_message))
        logger.info(msg=pformat(response_parameters))


if __name__ == "__main__":
    # This call will trigger the framework's input parser and its
    # output generator. Just add your call sign and your APRS message
    # text; the latter will then be processed by the input parser.
    testcall(message_text="error", from_callsign="DF1JSL-1")
