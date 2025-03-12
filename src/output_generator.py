#
# Core APRS Client: Output generator stub
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

from utils import make_pretty_aprs_messages


def generate_output_message(response_parameters: dict):
    """
    This is a stub for your custom APRS output generator

    Parameters
    ==========
    response_parameters: 'dict'
        dictionary object, containing data from input_parser.py
        Literally speaking, you will use the content from this
        dictionary in order to generate an APRS output message.
        For this stub, that dictionary is empty.

    Returns
    =======
    success: 'bool'
        True if everything is fine, False otherwise.
    output_message: 'list'
        List object, containing 0..n APRS output messages
        of up to 67 characters in length.
    """
    # Our stub code is always successful, so let's set the return
    # value accordingly
    success = True

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
    output_message = make_pretty_aprs_messages(message_to_add="Hello World!")

    # This is an example for adding an additional message part to the list item
    # Simply pass the list item as input parameter to our function, thus telling it
    # that you rather want to add additional content than having it create a new
    # list item for you
    output_message = make_pretty_aprs_messages(
        message_to_add="How are you...", destination_list=output_message
    )

    return success, output_message


if __name__ == "__main__":
    pass
