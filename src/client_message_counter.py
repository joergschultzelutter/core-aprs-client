#
# Core APRS Client
# Wrapper for message counter functions
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
from client_logger import logger
from client_utils import build_full_pathname


class APRSMessageCounter:
    def __init__(self, file_name: str):
        """
        This class implements the APRS message counter.

        Parameters
        ==========
        file_name: 'str'
           External file where the APRS message counter is stored.

        Returns
        =======

        """

        # Init our future numeric counter
        self.counter = 0

        # sef the counter's local file name
        self.file_name: str = build_full_pathname(file_name=file_name)

        # and finally, (try to) read the file from disk
        self.read_counter()

    def read_counter(self):
        """
        Reads the latest message counter from a file
        and sets the class' internal counter

        If file is not present, we will start with '0'

        Parameters
        ==========

        Returns
        =======

        """

        logger.debug(msg="Creating APRS message counter object...")

        # Initially, assume that our source file does not exist
        self.counter = 0

        try:
            with open(f"{self.file_name}", "r") as f:
                if f.mode == "r":
                    contents = f.read()
                    f.close()
                    self.counter = int(contents)
        except (FileNotFoundError, Exception):
            self.counter = 0
            logger.debug(
                msg=f"Cannot read content from message counter file {self.file_name}; will create a new file"
            )

    def write_counter(self):
        """
        Writes the latest message counter to a file

        Parameters
        ==========

        Returns
        =======

        """
        logger.debug(msg="Writing APRS message counter object to disk ...")
        try:
            with open(f"{self.file_name}", "w") as f:
                f.write("%d" % self.counter)
                f.close()
        except (IOError, OSError):
            logger.debug(msg=f"Cannot write message counter to {self.file_name}")

    def get_counter(self):
        """
        Getter method for the counter

        Parameters
        ==========

        Returns
        =======
        counter: 'int'
            Our numeric APRS counter

        """
        return self.counter

    def set_counter(self, counter: int):
        """
        Setter method for the counter

        Parameters
        ==========
        counter: 'int'
            Our numeric APRS counter

        Returns
        =======

        """
        if type(counter) is int:
            self.counter = counter
        else:
            raise ValueError("Value type must be int")


if __name__ == "__main__":
    pass
