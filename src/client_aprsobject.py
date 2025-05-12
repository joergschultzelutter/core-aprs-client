#
# Core APRS Client
# Wrapper for APRS-IS communication
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
from client_logger import logger
import aprslib


class APRSISObject:
    def __init__(
        self, aprsis_callsign, aprsis_passwd, aprsis_host, aprsis_port, aprsis_filter
    ):
        """
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
        """
        self.aprsis_callsign = aprsis_callsign
        self.aprsis_passwd = aprsis_passwd
        self.aprsis_host = aprsis_host
        self.aprsis_port = aprsis_port
        self.aprsis_filter = aprsis_filter
        self.AIS: aprslib.inet.IS = None

        self.ais_open()

    def ais_open(self):
        """
        Helper method for creating the APRS-IS object

        Parameters
        ==========
        self.aprsis_callsign: 'str'
           Our login callsign
        self.aprsis_passwd: 'str'
           Our login password
        self.aprsis_host: 'str'
           Our login hostname
        self.aprsis_port: 'int'
           Our APS-IS port number
        self.aprsis_filter: 'str'
           Our APRS-IS filter settings

        Returns
        =======
        self.AIS: 'aprslib.inet.IS'
           Our APRS-IS object
        """

        logger.debug(
            msg=f"Configuring APRS object: server={self.aprsis_host}, port={self.aprsis_port}, filter={self.aprsis_filter}, APRS-IS passcode={self.aprsis_passwd}, APRS-IS User = {self.aprsis_callsign}"
        )

        self.AIS = aprslib.IS(
            callsign=self.aprsis_callsign,
            passwd=self.aprsis_passwd,
            host=self.aprsis_host,
            port=self.aprsis_port,
        )
        if self.AIS:
            self.AIS.set_filter(self.aprsis_filter)

        return self.AIS

    def ais_start_consumer(self, aprsis_callback: object):
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
        if type(self.AIS) is aprslib.inet.IS:
            self.AIS.consumer(aprsis_callback, blocking=True, immortal=True, raw=False)
        else:
            logger.debug(msg="Not connected to APRS-IS")

    def ais_connect(self):
        """
        Helper method for connecting to the APRS-IS server

        Parameters
        ==========

        Returns
        =======
        """
        if type(self.AIS) is aprslib.inet.IS:
            self.AIS.connect(blocking=True)

    def ais_is_connected(self):
        """
        Helper method for returning the current connection
        state to the user. Yes, this accesses a protected element
        from the aprslib.inet.IS object, but it still works :-)

        Parameters
        ==========

        Returns
        =======
        """
        if type(self.AIS) is aprslib.inet.IS:
            return self.AIS._connected
        else:
            return False

    def ais_close(self):
        """
        Helper method for closing the APRS-IS connection

        Parameters
        ==========

        Returns
        =======
        """
        # Close APRS-IS connection whereas still present
        if type(self.AIS) is aprslib.inet.IS:
            logger.debug(msg="Closing connection to APRS-IS")
            self.AIS.close()
            self.AIS = None
        else:
            logger.debug(msg="Not connected to APRS-IS")

    def ais_send(self, aprsis_data: str):
        """
        Helper method for starting the APRS-IS consumer

        Parameters
        ==========
        aprsis_data: 'str'
           The data that we want to send to the APRS-IS server

        Returns
        =======
        """
        if type(self.AIS) is aprslib.inet.IS:
            self.AIS.sendall(aprsis_data)
        else:
            logger.debug(msg="Not connected to APRS-IS")

    def ais_get(self):
        """
        Helper method for getting the APRS-IS consumer object

        Parameters
        ==========

        Returns
        =======
        self.AIS: 'aprslib.inet.IS'
            Our APRS-IS object (or 'None')

        """
        if type(self.AIS) is aprslib.inet.IS:
            return self.AIS
        else:
            return None


if __name__ == "__main__":
    pass
