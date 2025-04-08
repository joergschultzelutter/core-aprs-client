#
# Core APRS Client: Wrapper for APRS-IS communication
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
import logging
import aprslib

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(module)s -%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

#
# The variable which holds our future AIS object
AIS: aprslib.inet.IS = None


def ais_open(
    aprsis_callsign: str,
    aprsis_passwd: str,
    aprsis_host: str,
    aprsis_port: int,
    aprsis_filter: str,
):
    """
    Helper method for creating the APRS-IS object

    Parameters
    ==========
    aprsis_callsign: 'str'
       Our login callsign
    aprsis_passwd: 'str'
       Our login password
    aprsis_host: 'str'
       Our login hostname
    aprsis_port: 'int'
       Our APS-IS port number
    aprsis_filter: 'str'
       Our APRS-IS filter settings

    Returns
    =======
    """

    global AIS
    AIS = aprslib.IS(
        callsign=aprsis_callsign,
        passwd=aprsis_passwd,
        host=aprsis_host,
        port=aprsis_port,
    )
    if AIS:
        AIS.set_filter(aprsis_filter)


def ais_start_consumer(aprsis_callback: object):
    """
    Helper method for starting the APRS-IS consumer

    Parameters
    ==========
    aprsis_callback: 'object'
       The name of our callback function that we hand over
       to the APRS-IS object

    Returns
    =======
    """
    global AIS
    if AIS:
        AIS.consumer(aprsis_callback, blocking=True, immortal=True, raw=False)


def ais_connect():
    """
    Helper method for connecting to the APRS-IS server

    Parameters
    ==========

    Returns
    =======
    """
    global AIS
    if AIS:
        AIS.connect(blocking=True)


def ais_is_connected():
    def ais_connect():
        """
        Helper method for returning the current connection
        state to the user. Yes, this accesses a protected element
        from the aprslib.inet.IS object, but it still works :-)

        Parameters
        ==========

        Returns
        =======
        """

    global AIS
    return AIS._connected


def ais_close():
    """
    Helper method for closing the APRS-IS connection

    Parameters
    ==========

    Returns
    =======
    """
    global AIS
    # Close APRS-IS connection whereas still present
    if AIS:
        logger.info(msg="Closing connection to APRS-IS")
        AIS.close()
        AIS = None


def ais_send(aprsis_data: str):
    """
    Helper method for starting the APRS-IS consumer

    Parameters
    ==========
    aprsis_data: 'str'
       The data that we want to send to the APRS-IS server

    Returns
    =======
    """
    global AIS
    if AIS:
        AIS.sendall(aprsis_data)


if __name__ == "__main__":
    pass
