#
# Core APRS Client: Wrapper for configparser data
# Author: Joerg Schultze-Lutter, 2025
#
# aprslib does not allow us to pass additional parameters to its
# callback function. Therefore, this module acts as a pseudo object in
# order to encapsulate the client configuration data
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
import configparser
from utils import check_if_file_exists

config = configparser.ConfigParser()
program_config = {}


def load_config(config_file: str = "core_aprs_client.cfg"):
    if check_if_file_exists(config_file):
        config.read(config_file)
        config_to_dict(config)
    else:
        program_config.clear()


def str_to_bool(value: str):
    return value.lower() in ("true", "yes", "on", "1")


def config_to_dict(config: configparser.ConfigParser):
    program_config.clear()
    for section in config.sections():
        program_config[section] = {
            key: str_to_bool(value)
            if value.lower() in ("true", "false", "yes", "no", "on", "off", "1", "0")
            else value
            for key, value in config[section].items()
        }
        return program_config


def get_config():
    return program_config
