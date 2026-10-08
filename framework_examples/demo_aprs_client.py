#
# Core APRS Client
# Sample APRS Client stub, using the core-aprs-client framework
# Author: Joerg Schultze-Lutter, 2025
#
# This demo client imports the input parser and output processor
# functions and establishes a live connection to APRS-IS
#
# Demo of class method:
# https://github.com/joergschultzelutter/core-aprs-client/blob/apprise-messaging-method/docs/coreaprsclient_class.md#activate_client-class-method
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
from collections.abc import Callable
from typing import Any
import subprocess

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
    __configfile: str
        name of the configuration file
    __daemon: bool
        run in daemon mode
    __logfile: str
        name of the log file (daemon mode only)
    __daemon_child: bool
        internally set when daemon mode is active
    """

    parser = argparse.ArgumentParser()

    # Config file name
    parser.add_argument(
        "--configfile",
        default="core_aprs_client.cfg",
        type=argparse.FileType("r"),
        help="Program config file name (default is 'core_aprs_client.cfg')",
    )

    # run as daemon yes/no
    parser.add_argument(
        "--daemon",
        default=False,
        action="store_true",
        help="Run as a daemon",
    )

    # logfile name
    parser.add_argument(
        "--logfile",
        default="nohup.out",
        help="Name of log file (only used with active daemon mode)",
    )

    # internal switch which will indicate to the spawned process
    # that no further spawning is necessary
    parser.add_argument(
        "--daemon-child",
        default=False,
        action="store_true",
        help=argparse.SUPPRESS,
    )

    # Parse the arguments
    args = parser.parse_args()

    # retrieve the parsed arguments
    __configfile = args.configfile.name
    __daemon = args.daemon
    __logfile = args.logfile
    __daemon_child = args.daemon_child

    # check if the log file exists
    if not os.path.isfile(__configfile):
        logger.error(msg=f"Config file '{__configfile}' does not exist; exiting")
        sys.exit(1)

    return __configfile, __daemon, __logfile, __daemon_child


def start_detached(configfile_name: str, logfile_name: str):
    """
    (Re)Starts the current program as a detached process

    Parameters
    ==========

    Returns
    =======
    """

    # Set the fully qualified filename to our Python program
    script_path = os.path.abspath(__file__)

    print(f"Spawning {script_path} into daemon mode ....")

    # Spawn the process
    with open(logfile_name, "ab", buffering=0) as log_file:
        p = subprocess.Popen(
            [
                sys.executable,
                script_path,
                "--daemon-child",
                "--configfile",
                configfile_name,
                "--logfile",
                logfile_name,
            ],
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
            cwd=os.getcwd(),
        )
        print(f"Process ID: {p.pid}")


def main():
    """
    Our main function

    Parameters
    ==========

    Returns
    =======
    """

    # Get the configuration file name
    configfile, daemon, logfile, daemon_child = get_command_line_params()

    # If daemon mode has been requested, spawn the process and then exit
    if daemon:
        start_detached(configfile_name=configfile, logfile_name=logfile)
        return

    # Startup code for both the spawned process and the standalone approach
    logger.info(msg=f"Starting demo module: APRS bot")
    logger.info(
        msg="This is a demo APRS client which connects to APRS-IS, listens to messages and processes them."
    )

    logger.info("My process ID is %s", os.getpid())

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

    # Activate the APRS client and connect to APRS-IS
    client.activate_client()


if __name__ == "__main__":
    main()
