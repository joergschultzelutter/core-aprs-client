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

import sys
import signal
import time
import atexit
import os
import types
from functools import partial

import client_shared
from client_utils import (
    get_command_line_params,
    signal_term_handler,
    check_and_create_data_directory,
    client_exception_handler,
    handle_exception,
    check_for_default_config,
)
from client_configuration import load_config, program_config
from client_aprsobject import APRSISObject
from client_message_counter import APRSMessageCounter
from client_expdict import create_expiring_dict
from client_aprs_communication import (
    aprs_callback,
    init_scheduler_jobs,
    remove_scheduler,
)
from client_logger import logger


class CoreAprsClient:
    config_file: str
    log_level: int
    input_parser: types.FunctionType
    output_generator: types.FunctionType

    def __init__(self, config_file: str, input_parser: types.FunctionType, output_generator: types.FunctionType, log_level: int):
        self.config_file = config_file
        self.input_parser = input_parser
        self.output_generator = output_generator
        self.log_level = log_level

    def run_listener(self):
        pass

    def testcall(self):
        pass

