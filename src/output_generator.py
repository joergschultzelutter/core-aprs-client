#
# Core APRS Client: Input parser stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is the module where you check the incoming APRS message and
# determine which actions the user wants you to do
# Currently, this is just a stub which you need to populate
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

from utils import make_pretty_aprs_messages


def generate_output_message(response_parameters: dict):
    success = True
    output_message = []
    return success, output_message


if __name__ == "__main__":
    pass
