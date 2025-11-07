#
# Core APRS Client
# APRS output generator stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is a stub for the module which generates the outgoing APRS message
# (based on what the user wants you to do)
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

# These keywords are STUBS which also assume that the data parameters (originating
# from the input_processor) are forwarded as a 'dict' object. You need to modify
# this code according to your very own use case.
#


def __process_greetme_keyword(data_parameters: dict):
    """
    This is a stub which takes the sender's call sign from the input
    parameters and generates a greeting message, e.g. "Hello DF1JSL-1"

    Parameters
    ==========
    data_parameters: dict
        dictionary object, containing data from input_parser.py
        as received by this module's generate_output_message function.

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
    output_message: str
        The output message that we want to return to the user.
    """

    # generate the output message
    output_message = f"Hello {data_parameters["from_callsign"]}"

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def __process_sayhello_keyword(data_parameters: dict):
    """
    This is a stub which generates a static "Hello World" message

    Parameters
    ==========
    data_parameters: dict
        dictionary object, containing data from input_parser.py
        as received by this module's generate_output_message function.
        (not used in this function)

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
    output_message: str
        The output message that we want to return to the user.
    """
    # generate the output message
    output_message = "Hello World"

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def __process_loremipsum_keyword(data_parameters: dict):
    """
    This is a stub which takes the sender's call sign from the input
    parameters and generates a really long "lorem ipsum" message
    which will be split up by the framework into multiple APRS messages.

    Parameters
    ==========
    data_parameters: dict
        dictionary object, containing data from input_parser.py
        as received by this module's generate_output_message function.
        (not used in this function)

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
    output_message: str
        The output message that we want to return to the user.
    """
    output_message = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

    # Finally, indicate to the main process that we were successful
    success = True

    return success, output_message


def generate_output_message(input_parser_response_object: dict | object, **kwargs):
    """
    This is a stub for your custom APRS output generator

    Parameters
    ==========
    input_parser_response_object: dict | object
        dictionary object, containing data from input_parser.py
        Literally speaking, you will use the content from this
        dictionary in order to generate an APRS output message.
        You can (and should!) customize this dict object but ensure that
        both input_parser and output_processor use the same structure
        Note that you can also return other objects such as classes. Just ensure that
        both input_parser and output_generator share the very same
        structure for this variable.
    **kwargs: dict
        Optional keyword arguments

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
        Unlike for the input processor, there are no edge cases that we need to take
        care of (e.g. ignoring incoming messages). Therefore, a simple true/false
        return code will suffice.
    output_message: str
        The output message that we want to return to the user.
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

    match input_parser_response_object["command_code"]:
        case "greetme":
            return __process_greetme_keyword(
                data_parameters=input_parser_response_object
            )
        case "sayhello":
            return __process_sayhello_keyword(
                data_parameters=input_parser_response_object
            )
        case "loremipsum":
            return __process_loremipsum_keyword(
                data_parameters=input_parser_response_object
            )
        case _:
            # Unless properly parsed via input processor, we should never reach this code
            # If we do, then there is a discrepancy between the input_processor's "command_code"
            # and the one that we have here.
            # If such a case should ever arise, core_aprs_client's callback function will simply
            # respond to the user's request with the default error message from the config file
            # --> program_config["client_config"]["aprs_input_parser_default_error_message"]
            return False, None


if __name__ == "__main__":
    pass
