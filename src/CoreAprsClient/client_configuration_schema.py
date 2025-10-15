#
# Core APRS Client
# Schema file for the configuration file parser
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

CONFIGURATION_SCHEMA = {
    "coac_client_config": {
        "aprsis_callsign": str,
        "aprsis_tocall": str,
        "aprs_client_name": str,
        "aprs_input_parser_default_error_message": str,
        "aprs_message_enumeration": str,
    },
    "coac_network_config": {
        "aprsis_server_name": str,
        "aprsis_server_port": int,
        "aprsis_passcode": int,
        "aprsis_server_filter": str,
    },
    "coac_beacon_config": {
        "aprsis_broadcast_beacon": bool,
        "aprsis_table": str,
        "aprsis_symbol": str,
        "aprsis_latitude": str,
        "aprsis_longitude": str,
        "aprsis_beacon_altitude_ft": int,
        "aprsis_beacon_interval_minutes": int,
    },
    "coac_bulletin_config": {
        "aprsis_broadcast_bulletins": bool,
        "aprsis_bulletin_interval_minutes": int,
    },
    "coac_crash_handler": {
        "apprise_config_file": str,
        "nohup_filename": str,
    },
    "coac_dupe_detection": {
        "msg_cache_max_entries": int,
        "msg_cache_time_to_live": int,
    },
    "coac_message_delay": {
        "packet_delay_message": float,
        "packet_delay_ack": float,
        "packet_delay_grace_period": float,
        "packet_delay_bulletin": float,
        "packet_delay_beacon": float,
    },
    "coac_testing": {
        "aprsis_enforce_unicode_messages": bool,
        "aprsis_simulate_send": bool,
    },
    "coac_data_storage": {
        "aprs_data_directory": str,
        "aprs_message_counter_file_name": str,
    }
}

if __name__ == "__main__":
    pass
