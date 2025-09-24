#
# Core APRS Client
# Wrapper for expiring dictionary / dupe detection
# Author: Joerg Schultze-Lutter, 2025
#
# aprslib does not allow us to pass additional parameters to its
# callback function. Therefore, this module acts as a pseudo object in
# order to provide global access to its worker variables
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
from .client_logger import logger

#
# This is our (future) global variable for the expiring dictionary
#
aprs_message_cache: ExpiringDict = None


# Helper method for creating our APRS message cache
def create_expiring_dict(max_len: int, max_age_seconds: int):
    """
    Helper method for creating the ExpiringDict

    Parameters
    ==========
    max_len: int
       Number of max dictionary entries
    max_age_seconds: int
       life span per entry in seconds

    Returns
    =======
    """

    global aprs_message_cache

    # Create the decaying APRS message cache. Any APRS message that is present in
    # this cache will be considered as a duplicate / delayed and will not be processed
    logger.debug(
        msg=f"APRS message dupe cache set to {str(max_len)} max possible entries and a TTL of {str(max_age_seconds / 60)} mins"
    )
    aprs_message_cache = ExpiringDict(
        max_len=max_len,
        max_age_seconds=max_age_seconds,
    )
    return aprs_message_cache


if __name__ == "__main__":
    pass
