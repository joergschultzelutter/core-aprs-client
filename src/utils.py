#
# Alexa-APRS Gateway: various utility routines
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
from expiringdict import ExpiringDict
from datetime import datetime
import hashlib
import os
import logging
from unidecode import unidecode
import argparse
import configparser

# this is the name of the  directory where we store
# our data files
data_directory = "data_files"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def add_aprs_message_to_cache(
    message_text: str, message_no: str, users_callsign: str, aprs_cache: ExpiringDict
):
    """
    Creates an entry in our expiring dictionary cache. Later on,
    we can check for this entry and see if a certain message has already been sent
    within the past x minutes (setting is specified as part of the definition of the
    ExpiringDict). If we find that entry in our list before that entry has expired,
    we will not send it out again and consider the request to be fulfilled
    Parameters
    ==========
    message_text: 'str'
        APRS message (as extracted from the original incoming message)
    message_no: 'str'
        APRS message number (or 'None' if not present)
    users_callsign: 'str'
        Call sign of the user who has sent this message
    aprs_cache: 'ExpiringDict'
        Reference to the ExpiringDict cache
    Returns
    =======
    aprs_cache: 'ExpiringDict'
        Reference to the ExpiringDict cache, now containing our entry
    """
    # Create message key which consists of:
    # - an md5-ed version of the message text (save some bytes on storage)
    #   Conversion to string is necessary; otherwise, the lookup won't work
    # - the user's call sign
    # - the message number (note that this field's content can be 'None')
    md5_hash = hashlib.md5(message_text.encode("utf-8")).hexdigest()
    key = (md5_hash, users_callsign, message_no)
    # Finally, build the key. Convert it to a tuple as the key needs to be immutable
    key = tuple(key)

    # Add the Key to our expiring cache. The datetime stamp is not used; we
    # just need to give the dictionary entry a value
    aprs_cache[key] = datetime.now()
    return aprs_cache


def does_file_exist(file_name: str):
    """
    Checks if the given file exists. Returns True/False.

    Parameters
    ==========
    file_name: str
                    our file name
    Returns
    =======
    status: bool
        True /False
    """
    return os.path.isfile(file_name)


def get_aprs_message_from_cache(
    message_text: str, message_no: str, users_callsign: str, aprs_cache: ExpiringDict
):
    """
    Checks for an entry in our expiring dictionary cache.
    If we find that entry in our list before that entry has expired,
    we consider the request to be fulfilled and will not process it again
    Parameters
    ==========
    message_text: 'str'
        APRS message (as extracted from the original incoming message)
    message_no: 'str'
        APRS message number (or 'None' if not present)
    users_callsign: 'str'
        Call sign of the user who has sent this message
    aprs_cache: 'ExpiringDict'
        Reference to the ExpiringDict cache
    Returns
    =======
    key: 'Tuple'
        Key tuple (or 'None' if not found / no longer present)
    """
    # Create message key which consists of:
    # - an md5-ed version of the message text (save some bytes on storage)
    #   Conversion to string is necessary; otherwise, the lookup won't work
    # - the user's call sign
    # - the message number (note that this field's content can be 'None')
    md5_hash = hashlib.md5(message_text.encode("utf-8")).hexdigest()
    key = (md5_hash, users_callsign, message_no)
    # Finally, build the key. Convert it to a tuple as the key needs to be immutable
    key = tuple(key)

    if key in aprs_cache:
        return key
    else:
        return None


def dump_string_to_hex(message_text_string: str):
    """
    Converts string to hex format and returns that content to the user.
    If we find that entry in our list before that entry has expired,
    we consider the request to be fulfilled and will not process it again
    Parameters
    ==========
    message_text_string: 'str'
        Text that needs to be converted
    Returns
    =======
    hex-converted text to the user
    """
    return "".join(hex(ord(c))[2:] for c in message_text_string)


def convert_text_to_plain_ascii(message_string: str):
    """
    Converts a string to plain ASCII
    Parameters
    ==========
    message_string: 'str'
        Text that needs to be converted
    Returns
    =======
    hex-converted text to the user
    """
    message_string = (
        message_string.replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    message_string = unidecode(message_string)
    return message_string


def get_command_line_params():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--configfile",
        default="core_aprs_client.yml",
        type=argparse.FileType("r"),
        help="Program config file name",
    )

    parser.set_defaults(run_aws_setup=False)
    args = parser.parse_args()

    configfile = args.core_aprs_client
    return configfile


def get_program_config_from_file(config_filename: str = "core_aprs_client.yml"):
    config = configparser.ConfigParser()

    success = False
    try:
        config.read(config_filename)
        aprsis_callsign = config.get("core_aprs_client_config", "aprsis_callsign")
        aprsis_tocall = config.get("core_aprs_client_config", "aprsis_tocall")
        aprsis_server_name = config.get("core_aprs_client_config", "aprsis_server_name")
        aprsis_server_port = config.get("core_aprs_client_config", "aprsis_server_port")
        aprsis_simulate_send = config.get(
            "core_aprs_client_config", "aprsis_simulate_send"
        )
        aprsis_passcode = config.get("core_aprs_client_config", "aprsis_passcode")
        msg_cache_max_entries = config.get(
            "core_aprs_client_config", "msg_cache_max_entries"
        )
        msg_cache_time_to_live = config.get(
            "core_aprs_client_config", "msg_cache_time_to_live"
        )
        msg_packet_delay = config.get("core_aprs_client_config", "msg_packet_delay")
        success = True
    except Exception as ex:
        logger.info(
            msg="Error in configuration file; Check if your config format is correct."
        )
        success = False
        aprsis_callsign = (
            aprsis_tocall
        ) = aprsis_server_name = aprsis_server_port = False
        aprsis_simulate_send = aprsis_passcode = msg_cache_max_entries = False
        msg_cache_time_to_live = msg_packet_delay = False

    return (
        aprsis_callsign,
        aprsis_tocall,
        aprsis_server_name,
        aprsis_server_port,
        aprsis_simulate_send,
        aprsis_passcode,
        msg_cache_max_entries,
        msg_cache_time_to_live,
        msg_packet_delay,
    )


if __name__ == "__main__":
    pass
