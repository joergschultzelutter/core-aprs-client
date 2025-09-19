#
# Core APRS Client
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

from enum import Enum

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

class CoreAprsClientInputParserStatus(Enum):
    PARSE_ERROR = -1
    PARSE_IGNORE = 0
    PARSE_OK = 1


if __name__ == "__main__":
    pass
