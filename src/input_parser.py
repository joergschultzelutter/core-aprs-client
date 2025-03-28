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

    # Let's build a very simple command line parser. Our parser will support
    # two commands:
    # Command #1 - "greetings" keyword
    #              Builds a string "Greetings " + callsign, then returns that
    #              string back to the APRS user
    #              Internal command code = "greetme"
    # Command #2 - "hello" keyword
    #              Sends a "Hello World" string to the user
    #              Internal command code = "sayhello"
    #
    # Due to simplicity reasons, the demo parser uses very crude code. For a 
    # production release, you rather might want to use e.g. regular expressions
    # for keyword parsing
        
    # Initially assume that the user has sent us no valid keyword
    # This will trigger the output parser's error handler, thus allowing it
    # to send usage instructions to the user
    success = False

    # now define a variable which later on tells the output processor what the
    # user expects from us. Per default, that variable is empty
    what = ""

    # The following variable is used in conjunction with error messages. Assuming
    # that your code was instructed to e.g. pull a WX report for Berlin/Germany and
    # failed to do so because of an invalid API key, you can then populate this variable
    # in case of command-specific errors. When populated, the text in this variable will
    # returned to the user. When NOT populated, the bot's default error message is 
    # returned to the user.
    # You can easily build your own error handling mechanisms in case this function
    # does not work for you
    command_specific_error_message = ""
    
    # Convert our APRS message string to lowercase
    aprs_message = aprs_message.lower()
    
    # START of crude input data parser
    if "greetings" in aprs_message:
        what = "greetme"
        success = True
    if "hello" in aprs_message:
        what = "sayhello"
        success = True
    
    # our target dictionary
    response_parameters = {
        "from_callsign": users_callsign,
        "command_specific_error_message": command_specific_error_message,
        "what": what,
    }

    return success, response_parameters


if __name__ == "__main__":
    pass
