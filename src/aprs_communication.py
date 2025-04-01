#
# Core APRS Client: various APRS routines
# Author: Joerg Schultze-Lutter, 2022
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

import aprslib
import logging
import time
from client_configuration import program_config
from utils import (
    make_pretty_aprs_messages,
    get_aprs_message_from_cache,
    add_aprs_message_to_cache,
)
from input_parser import parse_input_message
from output_generator import generate_output_message

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def send_ack(
    myaprsis: aprslib.inet.IS,
    users_callsign: str,
    source_msg_no: str,
    alias: str,
    tocall: str,
    packet_delay: float = 2.0,
    simulate_send: bool = True,
):
    """
    Send acknowledgment for received package to APRS_IS if
    a message number was present
    If 'simulate_send'= True, we still prepare the message but only send it to our log file
    Parameters
    ==========
    myaprsis: 'aprslib.inet.IS'
        Our aprslib object that we will use for the communication part
    users_callsign: 'str'
        Call sign of the user that has sent us the message
    source_msg_no: 'str'
        message number from user's request. Can be 'None'. In that case, we don't send a message acknowledgment to the user
        (normally, we should not enter this function at all if this value is 'None'. The safeguard will still stay in place)
    simulate_send: 'bool'
        If True: Prepare string but only send it to logger
    alias: 'str'
        Our APRS alias (COAC)
    packet_delay: 'float'
        Delay after sending out our APRS acknowledgment request
    tocall: 'str'
        This bot uses the default TOCALL ("APRS")

    Returns
    =======
    none
    """

    if source_msg_no:
        logger.info(msg="Preparing acknowledgment receipt")
        stringtosend = f"{alias}>{tocall}::{users_callsign:9}:ack{source_msg_no}"
        if not simulate_send:
            logger.info(msg=f"Sending acknowledgment receipt: {stringtosend}")
            myaprsis.sendall(stringtosend)
            time.sleep(packet_delay)
        else:
            logger.info(msg=f"Simulating acknowledgment receipt: {stringtosend}")


def send_aprs_message_list(
    myaprsis: aprslib.inet.IS,
    message_text_array: list,
    destination_call_sign: str,
    send_with_msg_no: bool,
    aprs_message_counter: int,
    external_message_number: str,
    simulate_send: bool = True,
    new_ackrej_format: bool = False,
    alias: str = "COAC",
    packet_delay: float = 10.0,
    tocall: str = "APRS",
):
    """
    Send a pre-prepared message list to to APRS_IS
    All packages have a max len of 67 characters
    If 'simulate_send'= True, we still prepare the message but only send it to our log file
    Parameters
    ==========
    myaprsis: 'aprslib.inet.IS'
        Our aprslib object that we will use for the communication part
    message_text_array: 'list'
        Contains 1..n entries of the content that we want to send to the user
    destination_call_sign: 'str'
        Target user call sign that is going to receive the message (usually, this
        is the user's call sign who has sent us the initial message)
    send_with_msg_no: 'bool'
        If True, each outgoing message will have its own message ID attached to the outgoing content
        If False, no message ID is added
    aprs_message_counter: int
        message_counter for messages that require to be ack'ed
    simulate_send: 'bool'
        If True: Prepare string but only send it to logger
    external_message_number: 'str'
        only used if we deal with the new ackrej format
    new_ackrej_format: 'bool'
        false: apply the old ack/rej logic as described in aprs101.pdf.
        We generate our own message id. The user's message ID
        (from the original request) will NOT be added to the
        outgoing message
        ---
        True: apply the new ack/rej logic as described
        in http://www.aprs.org/aprs11/replyacks.txt
        We generate our own message id. The user's message ID
        (from the original request) WILL be added to the
        outgoing message
    alias: 'str'
        Our APRS alias (COAC)
    packet_delay: 'float'
        Delay after sending out our APRS acknowledgment request
    tocall: 'str'
        This bot uses the default TOCALL ("APRS")

    Returns
    =======
    aprs_message_counter: 'int'
        new value for message_counter for messages that require to be ack'ed
    """
    for single_message in message_text_array:
        stringtosend = f"{alias}>{tocall}::{destination_call_sign:9}:{single_message}"
        if send_with_msg_no:
            alpha_counter = get_alphanumeric_counter_value(aprs_message_counter)
            stringtosend = stringtosend + "{" + alpha_counter
            if new_ackrej_format:
                stringtosend = stringtosend + "}" + external_message_number[:2]
            aprs_message_counter = aprs_message_counter + 1
            if (
                aprs_message_counter > 676 or alpha_counter == "ZZ"
            ):  # for the alphanumeric counter AA..ZZ, this is equal to "ZZ"
                aprs_message_counter = 0
        if not simulate_send:
            logger.info(msg=f"Sending response message '{stringtosend}'")
            myaprsis.sendall(stringtosend)
        else:
            logger.info(msg=f"Simulating response message '{stringtosend}'")
        time.sleep(packet_delay)
    return aprs_message_counter


def get_alphanumeric_counter_value(numeric_counter: int):
    """
    Calculate an alphanumeric
    Parameters
    ==========
    numeric_counter: 'int'
        numeric counter that is used for calculating the start value
    Returns
    =======
    alphanumeric_counter: 'str'
        alphanumeric counter that is based on the numeric counter
    """
    first_char = int(numeric_counter / 26)
    second_char = int(numeric_counter % 26)
    alphanumeric_counter = chr(first_char + 65) + chr(second_char + 65)
    return alphanumeric_counter


def send_beacon_and_status_msg(
    myaprsis: aprslib.inet.IS, aprs_beacon_messages: list, simulate_send: bool = True
):
    """
    Send beacon message list to APRS_IS
    If 'simulate_send'= True, we still prepare the message but only send it to our log file

    Parameters
    ==========
    myaprsis: 'aprslib.inet.IS'
        Our aprslib object that we will use for the communication part
    aprs_beacon_messages: list
        List of pre-defined APRS beacon messages
    simulate_send: 'bool'
        If True: Prepare string but only send it to logger

    Returns
    =======
    none
    """
    logger.info(msg="Reached beacon interval; sending beacons")
    for bcn in aprs_beacon_messages:
        stringtosend = (
            program_config["client_config"]["aprsis_callsign"]
            + ">"
            + program_config["client_config"]["aprsis_tocall"]
            + ":"
            + bcn
        )
        if not simulate_send:
            logger.info(msg=f"Sending beacon: {stringtosend}")
            myaprsis.sendall(stringtosend)
            time.sleep(program_config["message_delay"]["packet_delay_other"])
        else:
            logger.info(msg=f"Simulating beacons: {stringtosend}")


def send_bulletin_messages(
    myaprsis: aprslib.inet.IS, bulletin_dict: dict, simulate_send: bool = True
):
    """
    Sends bulletin message list to APRS_IS
    'Recipient' is 'BLNxxx' and is predefined in the bulletin's dict 'key'. The actual message
    itself is stored in the dict's 'value'.
    If 'simulate_send'= True, we still prepare the message but only send it to our log file

    Parameters
    ==========
    myaprsis: 'aprslib.inet.IS'
        Our aprslib object that we will use for the communication part
    bulletin_dict: 'dict'
        The bulletins that we are going to send upt to the user. Key = BLNxxx, Value = Bulletin Text
    simulate_send: 'bool'
        If True: Prepare string but only send it to logger

    Returns
    =======
    none
    """
    logger.info(msg="reached bulletin interval; sending bulletins")
    for recipient_id, bln in bulletin_dict.items():
        stringtosend = (
            program_config["client_config"]["aprsis_callsign"]
            + ">"
            + program_config["client_config"]["aprsis_tocall"]
            + f"::{recipient_id:9}:{bln}"
        )
        if not simulate_send:
            logger.info(msg=f"Sending bulletin: {stringtosend}")
            myaprsis.sendall(stringtosend)
            time.sleep(program_config["message_delay"]["packet_delay_other"])
        else:
            logger.info(msg=f"simulating bulletins: {stringtosend}")


# APRSlib callback
# Extract the fields from the APRS message, start the parsing process,
# execute the command and send the command output back to the user
def mycallback(raw_aprs_packet: dict):
    """
    aprslib callback; this is the core process that takes care of everything
    Parameters
    ==========
    raw_aprs_packet: 'dict'
        dict object, containing the raw APRS data
    Returns
    =======
    """
    global aprs_message_counter
    global aprs_message_cache
    global AIS

    # Get our relevant fields from the APRS message
    addresse_string = raw_aprs_packet.get("addresse")
    message_text_string = raw_aprs_packet.get("message_text")
    response_string = raw_aprs_packet.get("response")
    msgno_string = raw_aprs_packet.get("msgNo")
    from_callsign = raw_aprs_packet.get("from")
    format_string = raw_aprs_packet.get("format")
    ackMsgno_string = raw_aprs_packet.get("ackMsgNo")

    # lower the response in case we received one
    if response_string:
        response_string = response_string.lower()

    # Check if we need to deal with the old vs the new message format
    new_ackrej_format = True if ackMsgno_string else False

    # Check if this request supports a msgno
    msg_no_supported = True if msgno_string else False

    # User's call sign. read: who has sent us this message?
    if from_callsign:
        from_callsign = from_callsign.upper()

    if addresse_string:
        # Lets examine what we've got:
        # 1. Message format should always be 'message'.
        #    This is even valid for ack/rej responses
        # 2. Message text should contain content
        # 3. response text should NOT be ack/rej
        # Continue if both assumptions are correct
        if (
            format_string == "message"
            and message_text_string
            and response_string not in ["ack", "rej"]
        ):
            # This is a message that belongs to us

            # logger.info(msg=dump_string_to_hex(message_text_string))

            # Check if the message is present in our decaying message cache
            # If the message can be located, then we can assume that we have
            # processed (and potentially acknowledged) that message request
            # within the last e.g. 5 minutes and that this is a delayed / dupe
            # request, thus allowing us to ignore this request.
            aprs_message_key = get_aprs_message_from_cache(
                message_text=message_text_string,
                message_no=msgno_string,
                users_callsign=from_callsign,
                aprs_cache=aprs_message_cache,
            )
            if aprs_message_key:
                logger.debug(
                    msg="DUPLICATE APRS PACKET - this message is still in our decaying message cache"
                )
                logger.debug(
                    msg=f"Ignoring duplicate APRS packet raw_aprs_packet: {raw_aprs_packet}"
                )
            else:
                logger.debug(msg=f"Received raw_aprs_packet: {raw_aprs_packet}")

                # Send an ack if we DID receive a message number
                # and we DID NOT have received a request in the
                # new ack/rej format
                # see aprs101.pdf pg. 71ff.
                if msg_no_supported and not new_ackrej_format:
                    send_ack(
                        myaprsis=AIS,
                        simulate_send=program_config["testing"]["aprsis_simulate_send"],
                        alias=program_config["client_config"]["aprsis_callsign"],
                        tocall=program_config["client_config"]["aprsis_tocall"],
                        users_callsign=from_callsign,
                        source_msg_no=msgno_string,
                    )
                #
                # This is where the magic happens: Try to figure out what the user
                # wants from us. If we were able to understand the user's message,
                # 'success' will be true. In any case, the 'response_parameters'
                # dictionary will give us a hint about what to do next (and even
                # contains the parser's error message if 'success' != True)
                # input parameters: the actual message, the user's call sign and
                # the aprs.fi API access key for location lookups
                success, response_parameters = parse_input_message(
                    aprs_message=message_text_string,
                    from_callsign=from_callsign,
                )
                logger.info(msg=f"Input parser result: {success}")
                logger.info(msg=response_parameters)
                #
                # If the 'success' parameter is True, then we should know
                # by now what the user wants from us. Now, we'll leave it to
                # another module to generate the output data of what we want
                # to send to the user.
                # The result to this post-processor will be a general success
                # status code and a list item, containing the messages that are
                # ready to be sent to the user.
                #
                # parsing successful?
                if success:
                    # Generate the output message for the requested keyword
                    # The 'success' status is ALWAYS positive even if the
                    # message could not get processed - the inline'd error
                    # message counts as positive message content
                    success, output_message = generate_output_message(
                        response_parameters=response_parameters,
                    )
                # darn - we failed to hail the Tripods
                # this is the branch where the input parser failed to understand
                # the message. A possible reason: you sent a keyword which requires
                # an additional parameter but failed to send that one, too.
                # As we only parse but never process data in that input
                # parser, we sinply don't know what to do with the user's message
                # and get back to him with a generic response.
                else:
                    input_parser_error_message = response_parameters[
                        "input_parser_error_message"
                    ]
                    # Dump the HRM to the user if we have one
                    if input_parser_error_message:
                        output_message = make_pretty_aprs_messages(
                            message_to_add=f"{input_parser_error_message}",
                            add_sep=False,
                        )
                    # If not, just dump the link to the instructions
                    # This is the default branch which dumps generic information
                    # to the client whenever there is no generic error text from the input parser
                    else:
                        output_message = make_pretty_aprs_messages(
                            message_to_add="Sorry, did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client",
                            add_sep=False,
                        )
                        logger.info(
                            msg=f"Unable to process APRS packet {raw_aprs_packet}"
                        )

                # Send our message(s) to APRS-IS
                aprs_message_counter = send_aprs_message_list(
                    myaprsis=AIS,
                    simulate_send=program_config["testing"]["aprsis_simulate_send"],
                    message_text_array=output_message,
                    destination_call_sign=from_callsign,
                    send_with_msg_no=msg_no_supported,
                    aprs_message_counter=aprs_message_counter,
                    external_message_number=msgno_string,
                    new_ackrej_format=new_ackrej_format,
                )

                # We've finished processing this message. Update the decaying
                # cache with our message.
                # Store the core message data in our decaying APRS message cache
                # Dupe detection is applied regardless of the message's
                # processing status
                aprs_message_cache = add_aprs_message_to_cache(
                    message_text=message_text_string,
                    message_no=msgno_string,
                    users_callsign=from_callsign,
                    aprs_cache=aprs_message_cache,
                )


if __name__ == "__main__":
    pass
