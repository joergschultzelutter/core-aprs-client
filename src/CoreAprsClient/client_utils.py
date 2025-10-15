#
# Core APRS Client
# Various utility routines
# Author: Joerg Schultze-Lutter, 2025
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
import datetime
import hashlib
import os
from unidecode import unidecode
import argparse
import zipfile
import apprise
import re
from .client_configuration import program_config
from .client_logger import logger
import sys

# These are global variables which will be used
# in case of an uncaught exception where we send
# the host a final Apprise message along with the
# program's stack trace
exception_occurred = False
ex_type = ex_value = ex_traceback = None

# maximum APRS message lengths with and without trailing
# message number in the outgoing message
#
# When trailing message numbers are activated, the message
# ALWAYS ends with a trailing " (xx/yy)" string whereas
# xx - current message number
# yy - max message number
APRS_MSG_LEN_TRAILING = 59
APRS_MSG_LEN_NOTRAILING = 67


def _get_aprs_msg_len() -> int:
    """
    Internal helper function which determines the maximum length of a single APRS message.
    The corresponding value is dependent on whether the user has activated trailing
    message numbers for the outgoing APRS message or not.

    Parameters
    ==========

    Returns
    =======
    aprs_msg_len: int
        trailing message no enabled: 59
        trailing message no disabled: 67
    """
    if "__main__" not in sys.modules:
        return (
            APRS_MSG_LEN_TRAILING
            if program_config["coac_client_config"]["aprs_message_enumeration"]
            else APRS_MSG_LEN_NOTRAILING
        )
    else:
        return APRS_MSG_LEN_TRAILING


def add_aprs_message_to_cache(
    message_text: str, message_no: str, target_callsign: str, aprs_cache: ExpiringDict
):
    """
    Creates an entry in our expiring dictionary cache. Later on,
    we can check for this entry and see if a certain message has already been sent
    within the past x minutes (setting is specified as part of the definition of the
    ExpiringDict). If we find that entry in our list before that entry has expired,
    we will not send it out again and consider the request to be fulfilled
    Parameters
    ==========
    message_text: str
        APRS message (as extracted from the original incoming message)
    message_no: str
        APRS message number (or 'None' if not present)
    target_callsign: str
        Call sign of the user who has sent this message
    aprs_cache: ExpiringDict
        Reference to the ExpiringDict cache
    Returns
    =======
    aprs_cache: ExpiringDict
        Reference to the ExpiringDict cache, now containing our entry
    """
    # Create message key which consists of:
    # - an md5-ed version of the message text (save some bytes on storage)
    #   Conversion to string is necessary; otherwise, the lookup won't work
    # - the user's call sign
    # - the message number (note that this field's content can be 'None')
    md5_hash = hashlib.md5(message_text.encode("utf-8")).hexdigest()
    key = (md5_hash, target_callsign, message_no)
    # Finally, build the key. Convert it to a tuple as the key needs to be immutable
    key = tuple(key)

    # Add the Key to our expiring cache. The datetime stamp is not used; we
    # just need to give the dictionary entry a value
    aprs_cache[key] = datetime.datetime.now()
    return aprs_cache


def check_if_file_exists(file_name: str):
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
    message_text: str, message_no: str, target_callsign: str, aprs_cache: ExpiringDict
):
    """
    Checks for an entry in our expiring dictionary cache.
    If we find that entry in our list before that entry has expired,
    we consider the request to be fulfilled and will not process it again
    Parameters
    ==========
    message_text: str
        APRS message (as extracted from the original incoming message)
    message_no: str
        APRS message number (or 'None' if not present)
    target_callsign: str
        Call sign of the user who has sent this message
    aprs_cache: ExpiringDict
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
    key = (md5_hash, target_callsign, message_no)
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
    message_text_string: str
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
    message_string: str
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
    """
    Gets and returns the command line arguments

    Parameters
    ==========

    Returns
    =======
    configfile: str
        name of the configuration file
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--configfile",
        default="core_aprs_client.cfg",
        type=argparse.FileType("r"),
        help="Program config file name (default is 'core_aprs_client.cfg')",
    )

    args = parser.parse_args()

    configfile = args.configfile.name

    if not check_if_file_exists(file_name=configfile):
        logger.error(msg="Config file does not exist; exiting")
        sys.exit(0)

    return configfile


def build_full_pathname(
    file_name: str,
    root_path_name: str = os.path.abspath(os.getcwd()),
    relative_path_name: str = "data_files",
):
    """
    Build a full-grown path based on $CWD, an optional relative directory name and a file name.

    Parameters
    ==========
    file_name: str
        file name without path
    root_path_name: str
        relative path name that we are going to add.
    relative_path_name: str
        relative path name that we are going to add.

    Returns
    =======
    full_path_name: str
        full path, consisting of root path name, the relative path name and the file name
    """
    return os.path.join(root_path_name, relative_path_name, file_name)


def create_zip_file_from_log(log_file_name: str):
    """
    Creates a zip file from our current log file and
    returns the file name to the caller

    Parameters
    ==========
    log_file_name: str
        our file name, e.g. 'nohup.out'

    Returns
    =======
    success: bool
        True if we were able to create our zip file, otherwise false
    """

    # Check if the file actually exists
    if not log_file_name:
        return False, None
    if not check_if_file_exists(file_name=log_file_name):
        return False, None

    # get a UTC time stamp as reference and create the file name
    _utc = datetime.datetime.now(datetime.UTC)
    zip_file_name = datetime.datetime.strftime(
        _utc, "core_aprs_client_crash_dump_%Y-%m-%d_%H-%M-%S%z.zip"
    )

    # write the zip file to disk
    with zipfile.ZipFile(zip_file_name, mode="w") as archive:
        archive.write(log_file_name)

    # and return the file name
    return True, zip_file_name


def signal_term_handler(signal_number, frame):
    """
    Signal handler for SIGTERM signals. Ensures that the program
    gets terminated in a safe way, thus allowing all databases etc
    to be written to disk.
    Parameters
    ==========
    signal_number:
        The signal number
    frame:
        Signal frame
    Returns
    =======
    """

    logger.debug(msg="Received SIGTERM; forcing clean program exit")
    sys.exit(0)


def send_apprise_message(
    message_header: str,
    message_body: str,
    apprise_config_file: str,
    message_attachment: str = None,
):
    """
    Generates Apprise messages and triggers transmission to the user
    We will use this e.g. for post-mortem dumps in case the client is on the
    verge of crashing

    Parameters
    ==========
    message_header : str
        The message header that we want to send to the user
    message_body : str
        The message body that we want to send to the user
    apprise_config_file: str
        Apprise Yaml configuration file
    message_attachment: str
        The message attachment that we want to send to the user
        'None' if we don't want to send an attachment

    Returns
    =======
    success: bool
        True if successful
    """

    # predefine the output value
    success = False

    logger.debug(msg="Starting Apprise message processing")

    if not apprise_config_file or apprise_config_file == "NOT_CONFIGURED":
        logger.debug(msg="Skipping Apprise messaging; message file is not configured")
        return success

    if not check_if_file_exists(apprise_config_file):
        logger.error(
            msg=f"Apprise config file {apprise_config_file} does not exist; aborting"
        )
        return success

    if message_attachment and not check_if_file_exists(message_attachment):
        logger.debug("Attachment file missing; disabling attachments")
        message_attachment = None

    # Create the Apprise instance
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    config.add(apprise_config_file)

    # Make sure to add our config into our apprise object
    apobj.add(config)

    if not message_attachment:
        # Send the notification
        apobj.notify(
            body=message_body,
            title=message_header,
            tag="all",
            notify_type=apprise.NotifyType.FAILURE,
        )
    else:
        # Send the notification
        apobj.notify(
            body=message_body,
            title=message_header,
            tag="all",
            notify_type=apprise.NotifyType.FAILURE,
            attach=message_attachment,
        )

    success = True

    logger.debug(msg="Finished Apprise message processing")
    return success


def check_and_create_data_directory(
    root_path_name: str,
    relative_path_name: str,
):
    """
    Check if the data directory is present and create it, if necessary

    Parameters
    ==========
    root_path_name: str
        relative path name that we are going to add.
    relative_path_name: str
        relative path name that we are going to add.

    Returns
    =======
    success: bool
        False in case of error
    """
    success = True
    _data_directory = os.path.join(root_path_name, relative_path_name)
    if not os.path.exists(_data_directory):
        logger.debug(
            msg=f"Data directory {_data_directory} does not exist, creating ..."
        )
        try:
            os.mkdir(path=_data_directory)
        except OSError:
            logger.error(
                msg=f"Cannot create data directory {_data_directory}, aborting ..."
            )
            success = False
    else:
        if not os.path.isdir(_data_directory):
            logger.error(msg=f"{_data_directory} is not a directory, aborting ...")
            success = False
    return success


def make_pretty_aprs_messages(
    message_to_add: str,
    destination_list: list = None,
    max_len: int = _get_aprs_msg_len(),
    separator_char: str = " ",
    add_sep: bool = True,
    force_outgoing_unicode_messages: bool = False,
) -> list:
    """
    Pretty Printer for APRS messages. As APRS messages are likely to be split
    up (due to the 67 chars message len limitation), this function prevents
    'hard cuts'. Any information that is to be injected into message
    destination list is going to be checked wrt its length. If
    len(current content) + len(message_to_add) exceeds the max_len value,
    the content will not be added to the current list string but to a new
    string in the list.

    Example:

    current APRS message = 1111111111222222222233333333333444444444455555555556666666666

    Add String "Hello World !!!!" (16 chars)

    Add the string the 'conventional' way:

    Message changes to
    Line 1 = 1111111111222222222233333333333444444444455555555556666666666Hello W
    Line 2 = orld !!!!

    This function however returns:
    Line 1 = 1111111111222222222233333333333444444444455555555556666666666
    Line 2 = Hello World !!!!

    In case the to-be-added text exceeds 67 characters due to whatever reason,
    this function first tries to split up the content based on space characters
    in the text and insert the resulting elements word by word, thus preventing
    the program from ripping the content apart. However, if the content consists
    of one or multiple strings which _do_ exceed the maximum text len, then there
    is nothing that we can do. In this case, we will split up the text into 1..n
    chunks of text and add it to the list element.

    Known issues: if the separator_char is different from its default setting
    (space), the second element that is inserted into the list may have an
    additional separator char in the text

    Parameters
    ==========
    message_to_add: str
        message string that is to be added to the list in a pretty way
        If string is longer than 67 chars, we will truncate the information
    destination_list: list
        List with string elements which will be enriched with the
        'mesage_to_add' string. Default: empty list aka user wants new list
    max_len: int:
        Max length of the list's string len.
        The length is dependent on whether the user has activated trailing
        message number information in the outgoing message or not.
        When activated, the message length is 59 - otherwise, it is 67.
        _get_aprs_msg_len() auto-determines the appropriate value.
    separator_char: str
        Separator that is going to be used for dividing the single
        elements that the user is going to add
    add_sep: bool
        True = we will add the separator when more than one item
               is in our string. This is the default
        False = do not add the separator (e.g. if we add the
                very first line of text, then we don't want a
                comma straight after the location
    force_outgoing_unicode_messages: bool
        False = all outgoing UTF-8 content will be down-converted
                to ASCII content
        True = all outgoing UTF-8 content will sent out 'as is'

    Returns
    =======
    destination_list: list
        List array, containing 1..n human readable strings with
        the "message_to_add' input data
    """
    # Dummy handler in case the list is completely empty
    # or a reference to a list item has not been specified at all
    # In this case, create an empty list
    if not destination_list:
        destination_list = []

    # replace non-permitted APRS characters from the
    # message text as APRS-IS might choke on this content
    # Details: see APRS specification pg. 71
    message_to_add = re.sub("[{}|~]+", "", message_to_add)

    # Check if the user wants unicode messages. Default is ASCII
    if (
        not program_config["coac_testing"]["aprsis_enforce_unicode_messages"]
        and not force_outgoing_unicode_messages
    ):
        # Convert the message to plain ascii
        # Unidecode does not take care of German special characters
        # Therefore, we need to 'translate' them first
        message_to_add = convert_text_to_plain_ascii(message_string=message_to_add)

    # If new message is longer than max len then split it up with
    # max chunks of max_len bytes and add it to the array.
    # This should never happen but better safe than sorry.
    # Keep in mind that we only transport plain text anyway.
    if len(message_to_add) > max_len:
        split_data = message_to_add.split()
        for split in split_data:
            # if string is short enough then add it by calling ourself
            # with the smaller text chunk
            if len(split) < max_len:
                destination_list = make_pretty_aprs_messages(
                    message_to_add=split,
                    destination_list=destination_list,
                    max_len=max_len,
                    separator_char=separator_char,
                    add_sep=add_sep,
                    force_outgoing_unicode_messages=force_outgoing_unicode_messages,
                )
            else:
                # string exceeds max len; split it up and add it as is
                string_list = split_string_to_string_list(
                    message_string=split, max_len=max_len
                )
                for msg in string_list:
                    destination_list.append(msg)
    else:  # try to insert
        # Get very last element from list
        if len(destination_list) > 0:
            string_from_list = destination_list[-1]

            # element + new string > max len? no: add to existing string, else create new element in list
            if len(string_from_list) + len(message_to_add) + 1 <= max_len:
                delimiter = ""
                if len(string_from_list) > 0 and add_sep:
                    delimiter = separator_char
                string_from_list = string_from_list + delimiter + message_to_add
                destination_list[-1] = string_from_list
            else:
                destination_list.append(message_to_add)
        else:
            destination_list.append(message_to_add)

    return destination_list


def split_string_to_string_list(
    message_string: str, max_len: int = _get_aprs_msg_len()
):
    """
    Force-split the string into chunks of max_len size and return a list of
    strings. This function is going to be called if the string that the user
    wants to insert exceeds more than e.g. 67 characters. In this unlikely
    case, we may not be able to add the string in a pretty format - but
    we will split it up for the user and ensure that none of the data is lost

    Parameters
    ==========
    message_string: str
        message string that is to be divided into 1..n strings of 'max_len"
        text length
    max_len: int:
        Max length of the list's string len.
        The length is dependent on whether the user has activated trailing
        message number information in the outgoing message or not.
        When activated, the message length is 59 - otherwise, it is 67.
        _get_aprs_msg_len() auto-determines the appropriate value.

    Returns
    =======
    split_strings: list
        List array, containing 1..n strings with a max len of 'max_len'
    """
    split_strings = [
        message_string[index : index + max_len]
        for index in range(0, len(message_string), max_len)
    ]
    return split_strings


def parse_bulletin_data():
    """
    This function parses the bulletin messages from the configuration file,
    checks them for validity and then adds them to the global 'aprs_bulletin_messages'
    dictionary.

    Parameters
    ==========

    Returns
    =======
    """

    # our target directory
    aprs_bulletin_messages: dict = {}

    # Get the key and value from our configuration file's bulletin messages section
    for key, value in program_config["coac_bulletin_messages"].items():
        # Message populated and less than max APRS message length?
        # note: we do not use message enumeration for bulletins
        # therefore, the max length requirement is always fixed (67 bytes)
        if 0 < len(value) <= APRS_MSG_LEN_NOTRAILING:
            # Check if the identifier follows these APRS requirements:
            # 1) must start with fixed "BLN" string
            # 2) needs to be followed by 1..6 ASCII-7 characters and/or digits
            match = re.match(
                pattern=r"^bln[a-z0-9]{1,6}$", string=key, flags=re.IGNORECASE
            )
            if match:
                # We found a match. As a precaution, let's check if the user has
                # used characters in the actual message which are special to APRS
                match = re.findall(r"[{}|~]+", value)
                if match:
                    # Yes, we could remove those characters straight away but the
                    # idea behind this two-fold approach is to inform the user that
                    # ideally, the config file needs to get updated
                    logger.debug(
                        msg=f"APRS bulletin message '{key}': removing special APRS characters from 'value' setting; check your configuration file"
                    )
                    # Let's get rid of those control characters from the message
                    value = re.sub(r"[{}|~]+", "", value)
                # Convert the bulletin identifier to upperkey
                key = key.upper()
                # and add it to our dictionary in case it does not exist
                # and its lenght (after potential character replacements)
                # is still greater than zero
                if key not in aprs_bulletin_messages and len(value) > 0:
                    aprs_bulletin_messages[key] = value
        else:
            # return some clarification to the user on why we have decided to
            # ignore this particular configuration setting
            if len(key) > APRS_MSG_LEN_NOTRAILING:
                logger.debug(
                    f"Ignoring bulletin setting for '{key}'; value exceeds {APRS_MSG_LEN_NOTRAILING} characters. Check your configuration file"
                )
            else:
                logger.debug(f"Ignoring bulletin setting for '{key}'; value is empty")

    return aprs_bulletin_messages


def client_exception_handler():
    """
    This function will be called in case of a regular program exit OR
    an uncaught exception. If an exception has occurred, we will try to
    send out an Apprise message along with the stack trace to the user

    Parameters
    ==========

    Returns
    =======
    """

    if not exception_occurred:
        return

    client_name = program_config["coac_client_config"]["aprs_client_name"]

    # Send a message before we hit the bucket
    message_body = f"'{client_name}' process has crashed. Reason: {ex_value}"

    # Try to zip the log file if possible
    success, log_file_name = create_zip_file_from_log(
        program_config["coac_crash_handler"]["nohup_filename"]
    )

    # check if we can spot a 'nohup' file which already contains our status
    if log_file_name and check_if_file_exists(log_file_name):
        message_body = message_body + " (log file attached)"

    # send_apprise_message will check again if the file exists or not
    # Therefore, we can skip any further detection steps here
    send_apprise_message(
        message_header=f"'{client_name}' process has crashed",
        message_body=message_body,
        apprise_config_file=program_config["coac_crash_handler"]["apprise_config_file"],
        message_attachment=log_file_name,
    )


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler which is installed by the
    main process. We only do a few things:
    - remember that there has been an uncaught exception
    - save the exception type / value / tracebace

    Parameters
    ==========
    exc_type:
        exception type object
    exc_value:
        exception value object
    exc_traceback:
        exception traceback object

    Returns
    =======
    """

    global exception_occurred
    global ex_type
    global ex_value
    global ex_traceback

    # set some global values so that we know why the program has crashed
    exception_occurred = True
    ex_type = exc_type
    ex_value = exc_value
    ex_traceback = exc_traceback

    logger.debug(f"Core process has received uncaught exception: {exc_value}")

    # and continue with the regular flow of things
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def check_for_default_config():
    """
    Checks if the user tries to run the program with its default configuration
    Doing so does not abort the program but (for now) just generates an error on the command line
    level.

    Parameters
    ==========

    Returns
    =======
    """

    if program_config["coac_client_config"]["aprsis_tocall"] == "APRS":
        logger.error(
            msg="'aprsis_tocall' is still set to default config; change config file ASAP"
        )

    if program_config["coac_client_config"]["aprsis_callsign"] == "COAC":
        logger.error(
            msg="'aprsis_callsign' is still set to default config; change config file ASAP"
        )


def format_list_with_enumeration(mylistarray: list):
    """
    Adds a trailing enumeration to the list if the user has activated this configuration in
    the client's config file

    Parameters
    ==========

    Returns
    =======
    listitem: list
        Either formatted list (if more than one list entry was present) or
        the original list item
    """

    max_total_length = APRS_MSG_LEN_NOTRAILING
    annotation_length = APRS_MSG_LEN_NOTRAILING - APRS_MSG_LEN_TRAILING
    max_content_length = max_total_length - annotation_length

    # check if we have more than 99 entries. We always truncate the list (just to be
    # on the safe side) but whenever more than 99 entries were detected, we also supply
    # the user with a warning message and notify him about the truncation
    if len(mylistarray) > 99:
        logger.warning(
            msg="User has supplied list with more than 99 elements; truncating"
        )
        trimmed_listarray = mylistarray[:98]
        trimmed_listarray.append("[message truncated]")
    else:
        trimmed_listarray = mylistarray
    total = len(trimmed_listarray)

    # now let's add the enumeration to the list - but only if we have
    # more than one list item in our outgoing list
    if len(trimmed_listarray) > 1:
        formatted_list = []
        for i, s in enumerate(trimmed_listarray, start=1):
            annotation = f" ({i:02d}/{total:02d})"
            truncated = s[:max_content_length]
            padded = truncated.ljust(max_content_length)
            final = padded + annotation
            formatted_list.append(final)

        return formatted_list
    else:
        # return the original list to the user
        return trimmed_listarray


def finalize_pretty_aprs_messages(mylistarray: list) -> list:
    """
    Helper method which finalizes the prettified APRS messages
    and triggers the addition of the trailing message numbers (if
    activated by the user).

    Parameters
    ==========
    mylistarray: list
        List of APRS messages

    Returns
    =======
    listitem: list
        Either formatted list (if more than one list entry was present) or
        the original list item
    """
    if program_config["coac_client_config"]["aprs_message_enumeration"]:
        return format_list_with_enumeration(mylistarray=mylistarray)
    else:
        return mylistarray


if __name__ == "__main__":
    pass
