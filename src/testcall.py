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
)
from client_input_parser import parse_input_message
from client_output_generator import generate_output_message
import logging
from pprint import pformat
import sys
import atexit
from client_configuration import load_config, program_config

exception_occurred = False
ex_type = ex_value = ex_traceback = None

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def testcall(message_text: str, from_callsign: str):
    logger.info(msg=f"parsing message '{message_text}' for callsign '{from_callsign}'")

    success, response_parameters = parse_input_message(
        aprs_message=message_text, from_callsign=from_callsign
    )

    logger.info(msg=pformat(response_parameters))
    if success:
        # enrich our response parameters with all API keys that we need for
        # the completion of the remaining tasks. The APRS access details
        # are not known and will be set to simulation mode
        logger.info(msg="Response:")
        logger.info(msg=pformat(generate_output_message(response_parameters)))
    else:
        input_parser_error_message = response_parameters["input_parser_error_message"]
        # Dump the HRM to the user if we have one
        if input_parser_error_message:
            output_message = make_pretty_aprs_messages(
                message_to_add=f"{input_parser_error_message}",
                add_sep=False,
            )
        # If not, just dump the link to the instructions
        else:
            output_message = make_pretty_aprs_messages(
                message_to_add="Sorry, did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client",
                add_sep=False,
            )
        logger.info(output_message)
        logger.info(msg=pformat(response_parameters))


if __name__ == "__main__":

    # Get the command line params
    configfile = get_command_line_params()
    if not configfile:
        sys.exit(0)

    # load the program config from our external config file
    load_config(config_file=configfile)
    if len(program_config) == 0:
        logger.info(msg="Program config file is empty or contains an error; exiting")
        sys.exit(0)

    # Register the on_exit function to be called on program exit
    atexit.register(client_exception_handler)

    # Set up the exception handler to catch unhandled exceptions
    sys.excepthook = handle_exception

    # This call will trigger the framework's input parser and its
    # output generator. Just add your call sign and your APRS message
    # text; the latter will then be processed by the input parser.
    testcall(message_text="hello", from_callsign="DF1JSL-1")
