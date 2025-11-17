#
# Core APRS Client
# Sample APRS Client stub, using the core-aprs-client framework
# Author: Joerg Schultze-Lutter, 2025
#
# This demo client imports the input parser and output processor
# functions and establishes a live connection to APRS-IS. Additionally,
# post-processing code gets executed AFTER the APRS response was sent to
# the user. The post-processing code will ONLY get executed if the user
# sends the "postprocessor" command to the core-aprs-client instance
#
# Demo of class method:
# https://github.com/joergschultzelutter/core-aprs-client/blob/apprise-messaging-method/docs/coreaprsclient_class.md#activate_client-class-method
#
# Details on post-processing:
# https://github.com/joergschultzelutter/core-aprs-client/blob/postproc/docs/coreaprsclient_class.md#using-the-post-processor
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
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

# Your custom post processor
from post_processor import post_processing

import argparse
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_command_line_params():
    """
    Gets and returns the command line arguments

    Parameters
    ==========

    Returns
    =======
    cfg: str
        name of the configuration file
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--configfile",
        default="core_aprs_client.cfg",
        type=argparse.FileType("r"),
        help="Program config file name (default is 'core_aprs_client.cfg')",
    )

    args = parser.parse_args()

    cfg = args.configfile.name

    if not os.path.isfile(cfg):
        logger.error(msg=f"Config file '{cfg}' does not exist; exiting")
        sys.exit(0)

    return cfg


if __name__ == "__main__":
    logger.info(msg=f"Starting demo module: APRS bot with post processor")
    logger.info(
        msg="This is a demo APRS client which connects to APRS-IS, processes the incoming message, sends a response back to the client and finally executes post-processing code."
    )

    # Get the configuration file name
    configfile = get_command_line_params()

    # Create the CoreAprsClient object. Supply the
    # following parameters:
    #
    # - configuration file name
    # - log level (from Python's 'logging' package)
    # - function names for both input processor and output generator
    # - function name for the post processor
    #
    # Note: in order to trigger the post-processor, send the APRS message
    #       "postprocessor" to your core-aprs-client instance. This will tell
    #       the output generator to provide input data for the post processor
    #       which will then trigger the post-processing AFTER the APRS response
    #       has been sent back to the user
    #
    client = CoreAprsClient(
        config_file=configfile,
        log_level=logging.DEBUG,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
        post_processor=post_processing,
    )

    # Activate the APRS client and connect to APRS-IS
    client.activate_client()
