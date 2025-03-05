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
    If 'simulate_send'= True, we still prepare the message but only send it to our  log file
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
        Our APRS alias (AMZN)
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
    alias: str = "AMZN",
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
        Our APRS alias (AMZN)
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


def send_beacon_and_status_msg(myaprsis: aprslib.inet.IS, simulate_send: bool = True):
    """
    Send beacon message list to APRS_IS
    If 'simulate_send'= True, we still prepare the message but only send it to our log file

    Parameters
    ==========
    myaprsis: 'aprslib.inet.IS'
        Our aprslib object that we will use for the communication part
    simulate_send: 'bool'
        If True: Prepare string but only send it to logger

    Returns
    =======
    none
    """
    logger.info(msg="Reached beacon interval; sending beacons")
    for bcn in mpad_config.aprs_beacon_messages:
        stringtosend = f"{mpad_config.mpad_alias}>{mpad_config.mpad_aprs_tocall}:{bcn}"
        if not simulate_send:
            logger.info(msg=f"Sending beacon: {stringtosend}")
            myaprsis.sendall(stringtosend)
            time.sleep(mpad_config.packet_delay_other)
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
        stringtosend = f"{mpad_config.mpad_alias}>{mpad_config.mpad_aprs_tocall}::{recipient_id:9}:{bln}"
        if not simulate_send:
            logger.info(msg=f"Sending bulletin: {stringtosend}")
            myaprsis.sendall(stringtosend)
            time.sleep(mpad_config.packet_delay_other)
        else:
            logger.info(msg=f"simulating bulletins: {stringtosend}")


if __name__ == "__main__":
    pass
