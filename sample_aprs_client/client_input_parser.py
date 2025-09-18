#
# Core APRS Client
# APRS input parser stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is a stub forwhere you check the incoming APRS message and
# determine which actions the user wants you to do
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

from CoreAprsClient import CoreAprsClientInputParserStatus


def parse_input_message(aprs_message: str, from_callsign: str):
    """
    This is a stub for your custom APRS input parser.

    Parameters
    ==========
    aprs_message: str
        The APRS message that the user has provided us with (1..67
        bytes in length). Parse the content and figure out what
        the user wants you to do.
    from_callsign: str
        Ham radio callsign that sent the message to us.
        Might be required by the input processor e.g. in case you
        have to determine the from_callsign's latitude/longitude.

    Returns
    =======
    return_code: enum
        Appropriate return code value, originating from the
        CoreAprsClientInputParserStatus class
    input_parser_error_message: str
        if return_code is not PARSE_OK, this field can contain an optional
        error message (e.g. context-specific errors related to the
        keyword that was sent to the bot). If this field is empty AND
        return_code is NOT PARSE_OK, then the default error message will be returned.
    input_parser_response_object: dict | object
        Dictionary object where we store the data that is required
        by the 'output_generator' module for generating the APRS message.
        For this stub, that dictionary is empty.
        Note that you can also return other objects such as classes. Just ensure that
        both client_input_parser and client_output_generator share the very same
        structure for this variable.
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
    # Command #3 - "lorem" keyword
    #              Sends a really long "lorem ipsum" string to the user
    #              Internal command code = "loremipsum"
    # Command #4 - "error" keyword
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
    if "lorem" in aprs_message:
        # We found a valid command
        command_code = "loremipsum"
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
    # You can (and have to) amend this dict object so that it contains all fields
    # relevant for output processing. Ensure that both input parser and output processor
    # use the same dictionary structure.
    input_parser_response_object = {
        "from_callsign": from_callsign,
        "command_code": command_code,
    }

    # We support three possible return codes from the input parser:
    # PARSE_OK     - Input processor has identified keyword and is ready
    #                to continue. This is the desired default state
    #                Whenever the return code is PARSE_OK, then we should know
    #                by now what the user wants from us. Now, we'll leave it to
    #                another module to generate the output data of what we want
    #                to send to the user (client_output_generatpr.py).
    #                The result to this post-processor will be a general success
    #                status code and the message that is to be sent to the user.
    # PARSE_ERROR  - an error has occurred. Most likely, the external
    #                input processor was either unable to identify a
    #                keyword from the message OR a follow-up process has
    #                failed; e.g. the user has defined a wx keyword,
    #                requiring the sender to supply mandatory location info
    #                which was missing from the message. In any way, this signals
    #                the callback function that we are unable to process the
    #                message any further
    # PARSE_IGNORE - The message was ok but we are being told to ignore it. This
    #                might be the case if the user's input processor has a dupe
    #                check that is additional to the one provided by the
    #                core-aprs-client framework. Similar to PARSE_ERROR, we
    #                are not permitted to process this request any further BUT
    #                instead of sending an error message, we will simply ignore
    #                the request. Note that the core-aprs-client framework has
    #                already ack'ed the request at this point, thus preventing it
    #                from getting resend by APRS-IS over and over again.
    #
    # Note that you should refrain from using PARSE_IGNORE whenever possible - a
    # polite inquiry should always trigger a polite response :-) Nevertheless, there
    # might be use cases where you simply need to ignore a (technically valid) request
    # in your custom code.
    return_code = CoreAprsClientInputParserStatus.PARSE_OK if success else CoreAprsClientInputParserStatus.PARSE_ERROR

    return return_code, input_parser_error_message, input_parser_response_object


if __name__ == "__main__":
    pass
