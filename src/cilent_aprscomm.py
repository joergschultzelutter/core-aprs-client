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
AIS = None

def ais_open(callsign: str,passwd: str, host: str, port: int, filter: str):
    AIS = aprslib.IS(callsign=callsign,passwd=passwd,host=host,port=port)
    if AIS:
        AIS.set_filter(filter)

def ais_start_consumer(aprs_callback: object):
    if AIS:
        AIS.consumer(aprs_callback, blocking=True, immortal=True, raw=False)

def ais_connect():
    if AIS:
        AIS.connect(blocking=True)

def ais_is_connected():
    return AIS._connected

def ais_close:
    # Close APRS-IS connection whereas still present
    if AIS:
        logger.info(msg="Closing connection to APRS-IS")
        AIS.close()
        AIS = None

def ais_send(ais_data: str)
    if AIS:
        AIS.sendall(ais_data)

if __name__ == "__main__":
    pass
