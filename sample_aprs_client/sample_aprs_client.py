#
# Core APRS Client
# Sample APRS Client stub, using the core-aprs-client framework
# Author: Joerg Schultze-Lutter, 2025
#
# This is a demo client which shows you how to connect to APRS-IS
#
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
    configfile: str
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

    configfile = args.configfile.name

    if not os.path.isfile(configfile):
        print("Config file does not exist; exiting")
        sys.exit(0)

    return configfile


if __name__ == "__main__":

    # Get the configuration file name
    config_file = get_command_line_params()

    # Create the CoreAprsClient object. Supply the
    # following parameters:
    #
    # - configuration file name
    # - log level (from Python's 'logging' package)
    # - function names for both input processor and output generator
    #
    client = CoreAprsClient(
        config_file=config_file,
        log_level=logging.INFO,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
    )

    # Activate the APRS client and connect to APRS-IS
    client.activate_client()

    # Demo code for a dryrun testcall
    # Remove the 'activate_client' statement and uncomment the statement
    # below for 100% offline testing. The preconfigured example assumes that
    # callsign "DF1JSL-1" has sent the APRS message text "lorem" to your bot.
    # client.dryrun_testcall(message_text="lorem", from_callsign="DF1JSL-1")
