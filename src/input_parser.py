#
# Core APRS Client: Input parser stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is the module where you check the incoming APRS message and
# determine which actions the user wants you to do
# Currently, this is just a stub which you need to populate
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

from client_configuration import program_config


def parse_input_message(aprs_message: str, users_callsign: str):
    """
    This is a stub for your custom APRS input parser.

    Parameters
    ==========
    aprs_message: 'str'
        The APRS message that the user has provided us with (1..67
        bytes in length). Parse the content and figure out what
        the user wants you to do.
    users_callsign: 'str'
        Ham radio callsign that sent the message to us.

    Returns
    =======
    success: 'bool'
        True if everything is fine, False otherwise.
    response_parameters: 'dict'
        Dictionary object where we store the data that is required
        by the 'output_generator' module for generating the APRS message.
        For this stub, that dictionary is empty.
    """

    # tell the calling process that everything is fine
    success = True

    # our target dictionary
    response_parameters = {
        "from_callsign": users_callsign,
    }

    # Example for a very simple command line parser
    # xxx

    # here you would add data to the dictionary (e.g. lat/lon, wx-related stuff),
    # thus telling the output_generator processes later on what the user wants from us
    #
    #
    #

    return success, response_parameters


if __name__ == "__main__":
    pass
