#
# Core APRS Client
# Demo of the framework's Apprise messaging functions
#
# Demo of class method:
# https://github.com/joergschultzelutter/core-aprs-client/blob/apprise-messaging-method/docs/configuration_subsections/config_crash_handler.md
#
# For further details on Apprise, please visit
# https://www.github.com/caronc/apprise
#
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
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

import argparse
import os
import sys
import logging
from pprint import pformat

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
    logger.info(msg=f"Starting demo module: Apprise messaging")
    logger.info(
        msg="This is a demo APRS client which sends a fixed demo message via Apprise to 1..n messaging clients"
    )

    # Get the configuration file name
    configfile = get_command_line_params()

    # Create the CoreAprsClient object. Supply the
    # following parameters:
    #
    # - configuration file name
    # - log level (from Python's 'logging' package)
    # - function names for both input processor and output generator
    #
    client = CoreAprsClient(
        config_file=configfile,
        log_level=logging.DEBUG,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
    )

    # This sends a fixed test message to 1..n messenger
    # clients via Apprise. By omitting the apprise_cfg_file
    # value, we tell the framework to use the Apprise config
    # file name from core-aprs-client's config file (see
    # https://github.com/joergschultzelutter/core-aprs-client/blob/apprise-messaging-method/docs/configuration_subsections/config_crash_handler.md
    # for further info. Alternatively, you can specify your very own
    # Apprise configuration file name.
    #
    # Note that a missing Apprise config file will not result in an
    # error but simply generates a log file error instead. By examining
    # the given return code, you can still decide to abort your program
    # afterwards, if necessary

    client.send_apprise_message(
        msg_header="Hello from Apprise",
        msg_body="This is a demo message",
        msg_attachment=None,
        apprise_cfg_file=None,
    )
