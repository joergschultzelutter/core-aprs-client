#
# Core APRS Client
# APRS output generator stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is the module where you generate the outgoing APRS message
# (based on what the user wants you to do)
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

from client_utils import make_pretty_aprs_messages
from client_configuration import program_config


def __process_greetme_keyword(response_parameters: dict):
    # Not let's assume that your code has processed the user's request and
    # that you need to generate the output message.
    # 'make_pretty_aprs_messages' will do that job for you. Simply pass
    # your string to the function and you will receive a list object, containing
    # 1..n future APRS messages. For adding additional content to that message,
    # simply pass that list item along as 'destination list' parameter for all
    # following calls

    # generate our very first message; either pass an empty list item to the
    # function or omit the 'destination_list" parameter. In that case, the function
    # will create a list object for you
    output_message = make_pretty_aprs_messages(message_to_add="Hello")

    # This is an example for adding an additional message part to the list item
    # Simply pass the list item as input parameter to our function, thus telling it
    # that you rather want to add additional content than having it create a new
    # list item for you
    output_message = make_pretty_aprs_messages(
        message_to_add=response_parameters["from_callsign"],
        destination_list=output_message,
    )

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def __process_sayhello_keyword(response_parameters: dict):
    # Not let's assume that your code has processed the user's request and
    # that you need to generate the output message.
    # 'make_pretty_aprs_messages' will do that job for you. Simply pass
    # your string to the function and you will receive a list object, containing
    # 1..n future APRS messages. For adding additional content to that message,
    # simply pass that list item along as 'destination list' parameter for all
    # following calls

    # generate our very first message; either pass an empty list item to the
    # function or omit the 'destination_list" parameter. In that case, the function
    # will create a list object for you
    output_message = make_pretty_aprs_messages(message_to_add="Hello")

    # This is an example for adding an additional message part to the list item
    # Simply pass the list item as input parameter to our function, thus telling it
    # that you rather want to add additional content than having it create a new
    # list item for you
    output_message = make_pretty_aprs_messages(
        message_to_add="World", destination_list=output_message
    )

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def __process_loremipsum_keyword(response_parameters: dict):
    # This example shows a case where a really long string gets auto-separated
    # into multiple message chunks. Apart from its content, this example is
    # identical to __process_sayhello_keyword

    # generate our very first message; either pass an empty list item to the
    # function or omit the 'destination_list" parameter. In that case, the function
    # will create a list object for you
    output_message = make_pretty_aprs_messages(
        message_to_add="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
    )

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def generate_output_message(response_parameters: dict):
    """
    This is a stub for your custom APRS output generator

    Parameters
    ==========
    response_parameters: dict
        dictionary object, containing data from client_input_parser.py
        Literally speaking, you will use the content from this
        dictionary in order to generate an APRS output message.
        You can (and should!) customize this dict object but ensure that
        both input_parser and output_processor use the same structure

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
    output_message: list
        List object, containing 0..n APRS output messages
        of up to 67 characters in length.
    """

    # This output generator stub is capable of processing two
    # commands:
    # Command #1 - "greetings" keyword
    #              Builds a string "Greetings " + callsign, then returns that
    #              string back to the APRS user
    #              Internal command code = "greetme"
    # Command #2 - "hello" keyword
    #              Sends a "Hello World" string to the user
    #              Internal command code = "sayhello"
    # Command #3 - "lorem" keyword
    #              Sends a multiline "lorem ipsum" APRS message to the user
    #              Internal command code = "loremipsum"
    #
    # Every other keyword will result in an error message
    #
    # The output processor takes input from a dictionary that was prepared by the
    # input processor. Note that those cases where the input processor FAILED to
    # guess the user's intentions will NOT be sent to this module.

    match response_parameters["command_code"]:
        case "greetme":
            return __process_greetme_keyword(response_parameters=response_parameters)
        case "sayhello":
            return __process_sayhello_keyword(response_parameters=response_parameters)
        case "loremipsum":
            return __process_loremipsum_keyword(response_parameters=response_parameters)
        case _:
            # Unless properly parsed via input processor, we should never reach this code
            return False, make_pretty_aprs_messages(
                message_to_add=program_config["client_config"][
                    "aprs_input_parser_default_error_message"
                ]
            )


if __name__ == "__main__":
    pass
