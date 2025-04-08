#
# Core APRS Client: Wrapper for message counter functions
# Author: Joerg Schultze-Lutter, 2025
#
# aprslib does not allow us to pass additional parameters to its
# callback function. Therefore, this module acts as a pseudo object in
# order to provide global access to its worker variables
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
import logging
from utils import build_full_pathname

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class MutableInt:
    def __init__(self, value):
        self.value = value


# Our global message counter
aprs_message_counter = MutableInt(0)


def read_aprs_message_counter(file_name: str):
    """
    Reads the latest message counter from a file

    If file is not present, we will start with '0'

    Parameters
    ==========
    file_name: 'str'
        Name of the file we are going to read the data from

    Returns
    =======
    aprs_message_counter: 'MutableInt'
        last message counter (or '0')
    """
    global aprs_message_counter
    served_packages = 0
    absolute_path_filename = build_full_pathname(file_name=file_name)
    try:
        with open(f"{absolute_path_filename}", "r") as f:
            if f.mode == "r":
                contents = f.read()
                f.close()
                served_packages = int(contents)
    except (FileNotFoundError, Exception):
        served_packages = 0
        logger.info(
            msg=f"Cannot read content from message counter file {absolute_path_filename}; will create a new file"
        )

    aprs_message_counter.value = served_packages
    return aprs_message_counter


def write_aprs_message_counter(file_name: str):
    """
    Writes the latest message counter to a file

    Parameters
    ==========
    file_name: 'str'
        Name of the file we are going to read the data from

    Returns
    =======
    Nothing
    """
    global aprs_message_counter
    absolute_path_filename = build_full_pathname(file_name=file_name)
    try:
        with open(f"{absolute_path_filename}", "w") as f:
            f.write("%d" % aprs_message_counter.value)
            f.close()
    except (IOError, OSError):
        logger.info(msg=f"Cannot write message counter to {absolute_path_filename}")


if __name__ == "__main__":
    pass
