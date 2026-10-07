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

LOGFILE = "nohup.out"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def setup_logging(daemon_mode: bool = False):
    handlers = []

    if daemon_mode:
        handlers.append(logging.FileHandler(LOGFILE))
    else:
        handlers.append(logging.StreamHandler(sys.stdout))


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

    parser.add_argument(
        "--daemon",
        default=False,
        action="store_true",
        help="Run as a daemon",
    )
    parser.add_argument(
        "--logfile",
        default=LOGFILE,
        help="Name of log file",
    )
    parser.add_argument(
        "--daemon-child",
        default=False,
        action="store_true",
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()
    __configfile = args.configfile.name
    __daemon = args.daemon
    __logfile = args.logfile
    __daemon_child = args.daemon_child

    if not os.path.isfile(__configfile):
        logger.error(msg=f"Config file '{__configfile}' does not exist; exiting")
        sys.exit(1)

    return __configfile, __daemon, __logfile, __daemon_child


def start_detached(logfile_name: str):
    script_path = os.path.abspath(__file__)

    print(f"Spawning {script_path} into daemon mode ....")

    with open(logfile_name, "ab", buffering=0) as log_file:
        p = subprocess.Popen(
            [sys.executable, script_path, "--daemon-child"],
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
            cwd=os.getcwd(),
        )
        print(f"Process ID: {p.pid}")


def run_client_loop(
    cfg_file: str,
    log_level: int,
    input_parser: Callable[..., Any],
    output_generator: Callable[..., Any],
    pre_processor: Callable[..., Any] | None = None,
    post_processor: Callable[..., Any] | None = None,
    daemon_mode: bool = False,
):

    setup_logging(daemon_mode=daemon_mode)
    logger.info("My process ID is %s", os.getpid())

    # Create the CoreAprsClient object. Supply the
    # following parameters:
    #
    # - configuration file name
    # - log level (from Python's 'logging' package)
    # - function names for both input processor and output generator
    #
    client = CoreAprsClient(
        config_file=cfg_file,
        log_level=log_level,
        input_parser=input_parser,
        output_generator=output_generator,
    )

    # Activate the APRS client and connect to APRS-IS
    client.activate_client()


def main():
    # Get the configuration file name
    configfile, daemon, logfile, daemon_child = get_command_line_params()

    if daemon:
        start_detached(logfile_name=logfile)
        return

    logger.info(msg=f"Starting demo module: APRS bot")
    logger.info(
        msg="This is a demo APRS client which connects to APRS-IS, listens to messages and processes them."
    )

    run_client_loop(
        cfg_file=configfile,
        log_level=logging.DEBUG,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
        daemon_mode=daemon_child,
    )


if __name__ == "__main__":
    main()
