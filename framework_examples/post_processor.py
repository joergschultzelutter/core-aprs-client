#
# Core APRS Client
# APRS post processor stub
# Author: Joerg Schultze-Lutter, 2025
#
# This is a stub for the module which generates the outgoing APRS message
# (based on what the user wants you to do)
#
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

# These keywords are STUBS which also assume that the data parameters (originating
# from the input_processor) are forwarded as a 'dict' object. You need to modify
# this code according to your very own use case.
#

from CoreAprsClient import CoreAprsClient
from pprint import pformat


def post_processing(
    instance: CoreAprsClient, postprocessor_input_object: dict | object, **kwargs
):
    """
    This is a stub for your custom APRS post processor code.

    Parameters
    ==========
    instance: CoreAprsClient
        Instance of the core-aprs-client object.
    postprocessor_input_object: dict | object
        Use this parameter for transporting data structures from the output generator
        to your custom post-processor code. Note that in order to get
        triggered, a) the post-processor code function needs to be supplied
        to the instantiated class object AND b) postprocessor_input_object
        must not be 'None'
        For the framework examples, this stub deliberately uses a simple
        dictionary for passing data from the output generator to the post
        processor. One could use a more complex dict object (just like the one used
        by input processor and output generator) - or a simple string. Again, what
        you want to use is up to you, the developer.
    **kwargs: dict
        Optional keyword arguments

    Returns
    =======
    success: bool
        True if everything is fine, False otherwise.
    """

    if postprocessor_input_object:
        instance.log_debug(msg="Executing post-processor")
        instance.send_apprise_message(
            msg_header="Hello World", msg_body="Executing post-processor code"
        )

    return True


if __name__ == "__main__":
    pass
