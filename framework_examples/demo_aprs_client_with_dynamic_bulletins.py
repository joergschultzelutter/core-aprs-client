#
# Core APRS Client
# Sample APRS Client stub, using the core-aprs-client framework
# Author: Joerg Schultze-Lutter, 2025
#
# This demo client imports the input parser and output processor
# functions and establishes a live connection to APRS-IS. It uses
# an additional scheduler job for feeding additional bulletin data
# to the APRS bulletin routines.
#
#
#
# !!!!!!
# It is strongly recommended to run this program in 'simulated' mode
# only, thus preventing any data from ending up on APRS-IS. Set
# 'aprsis_simulate_send' = 'true' and all is well. See comments below.
# !!!!!!
#
#
#
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
import random
import string
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_demo_dict():
    """
    Creates a random number of BLNxDEMO bulletins with random content

    Parameters
    ==========

    Returns
    =======
    demo_dict: dict
        target dictionary with random bulletins
    """
    demo_dict = {}
    num_keys = random.randint(1, 10)

    for i in range(num_keys):
        key = f"BLN{i}DEMO"
        target_length = random.randint(1, 67)

        words = []
        total_length = 0

        while total_length < target_length:
            word_length = random.randint(2, 8)
            word_chars = random.choices(
                string.ascii_letters + string.digits, k=word_length
            )
            word = "".join(word_chars)

            word = word[0].upper() + "".join(
                random.choice([c.upper(), c.lower()]) for c in word[1:]
            )

            if total_length + len(word) + len(words) > target_length:
                break

            words.append(word)
            total_length += len(word)

        # Fallback in case nothing was generated
        if not words:
            words.append(
                "".join(
                    random.choices(
                        string.ascii_uppercase + string.digits, k=target_length
                    )
                )
            )

        value = "-".join(words)[:target_length]
        demo_dict[key] = value

    return demo_dict


def make_demo_beacon(myclient: CoreAprsClient):
    """
    This is a simple "setter" method which will first generate a dictionary
    with random bulletins and then add them to the target dictionary. It gets called
    by the main program's scheduler job.

    Parameters
    ==========

    Returns
    =======

    """
    myclient.dynamic_aprs_bulletins = create_demo_dict()


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
        print("Config file does not exist; exiting")
        sys.exit(0)

    return cfg


if __name__ == "__main__":

    logger.info(msg=f"Starting {__name__}")
    logger.info(
        msg="This is a demo APRS client which connects to APRS-IS and extends the set of static bulletins with dynamic bulletin data"
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

    # Create the scheduler object which will handle the updates to our
    # class' dictionary item
    my_scheduler = BackgroundScheduler()

    # Add the scheduler job. We will simply create 1..10 additional bulletins,
    # following a BLN{x}DEMO pattern. Each entry will consist of 1..67 random
    # characters and digits. Remember, this is for demonstration purposes only.
    #
    # For this demo, the job is executed every 45 seconds.
    #
    # URGENT word of advice: I strongly recommend NOT sending these bulletins to APRS-IS,
    # ESPECIALLY not with the preconfigured execution interval. If you send this
    # as live data, your account is likely going to get blocked.
    #
    # For offline testing purposes, the follwing settings in the configuration file
    # are recommended:
    #
    # 'aprsis_simulate_send' = 'true'
    # 'aprsis_bulletin_interval_minutes' = 1 (--> minutes)
    #
    # The framework will still generate the bulletin data every minute. However, by
    # activating 'aprsis_simulate_send', no data will be sent to APRS-IS.
    #
    # Add the scheduler job to the scheduler; demo (offline) interval is 45 seconds
    # Every interval, we will create 1..9 bulletin items with random content and add the
    # encapsulating dictionary to the CoreAprsClient class object, thus exposing these
    # items to the handler that takes care of the static bulletins from the
    # configuration file
    my_scheduler.add_job(
        make_demo_beacon,
        "interval",
        id="beacondemo",
        seconds=45,
        args=[
            client,
        ],
        max_instances=1,
        coalesce=True,
    )

    # start the scheduler
    my_scheduler.start()

    # As we safely want to remove the scheduler in case of ctrl-c or server shutdown,
    # let's add an exception handler
    try:
        # Activate the APRS client and connect to APRS-IS
        client.activate_client()
    except (KeyboardInterrupt, SystemExit):

        # Pause the scheduler and remove all jobs afterwards.
        my_scheduler.pause()
        my_scheduler.remove_all_jobs()
