#
# Core APRS Client
# APRS input parser stub
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


def parse_input_message(aprs_message: str, from_callsign: str):
    """
    This is a stub for your custom APRS input parser.

    Parameters
    ==========
    aprs_message: 'str'
        The APRS message that the user has provided us with (1..67
        bytes in length). Parse the content and figure out what
        the user wants you to do.
    from_callsign: 'str'
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
    # Command #3 - "error" keyword
    #              Simulates an error (e.g. missing keyword parameter)
    #              Internal command code = "sayhello"
    #
    # Due to simplicity reasons, the demo parser uses very crude code. For a
    # production release, you rather might want to use e.g. regular expressions
    # for keyword parsing
    #
    # The internal command code will tell the output processor what to do. For mere
    # illustration purposes, this code stub's internal command codes differ from
    # the user's input (via the APRS message)

    # Initially assume that the user has sent us no valid keyword
    # This will trigger the output parser's error handler, thus allowing it
    # to send usage instructions to the user
    success = False

    # now define a variable which later on tells the output processor what the
    # user expects from us. Per default, that variable is empty
    command_code = ""

    # The following variable is used in conjunction with errors during parsing.
    # Assuming that e.g. your keyword is used for pulling a wx report for a certain
    # city but the user forgot to specify that additional parameter, you can use this
    # variable. By populating it, core-aprs-client will output THIS variable's content
    # to the user whenever 'success == False' applies. If that variable is empty, the
    # bot's default error message will be used instead.
    # You can easily build your own error handling mechanisms in case this function
    # does not work for you
    input_parser_error_message = ""

    # Convert our APRS message string to lowercase
    aprs_message = aprs_message.lower()

    # START of super crude input data parser
    if "greetings" in aprs_message:
        # We found a valid command
        command_code = "greetme"
        success = True
    if "hello" in aprs_message:
        # We found a valid command
        command_code = "sayhello"
        success = True
    if "error" in aprs_message:
        # Simulate that we did NOT find a valid command
        # Instead of using a default error message, we will use the
        # value from the 'input_parser_error_message' instead.
        #
        # Note that whenever 'success == False', these commands will
        # NOT be sent to the output processor for further processing.
        # We did not figure out what the user wants from us, therefore
        # there is nothing that we can do for the user.
        #
        # if 'input_parser_error_message' is pupulated AND 'success == False',
        # the content from 'input_parser_error_message' will be returned to
        # the user. If 'input_parser_error_message' is empty AND 'success == False',
        # then the default error message will be sent to the user.
        #
        input_parser_error_message = "Triggered input processor error"
        success = False

    # our target dictionary that is going to be used by the output processor
    # for further processing.
    response_parameters = {
        "from_callsign": from_callsign,
        "input_parser_error_message": input_parser_error_message,
        "command_code": command_code,
    }

    return success, response_parameters


if __name__ == "__main__":
    pass
