# core-aprs-client

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![PyPi version](https://img.shields.io/pypi/v/core-aprs-client.svg)](https://pypi.python.org/pypi/core-aprs-client)

Core APRS client framework with dupe detection, bulletin/beaconing support, and other APRS-IS related stuff.

```core-aprs-client``` is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s APRS functions which can be used for building your very own APRS client / bot. Its framework supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS messaging functions, such as connecting to APRS-IS, message dupe detection, ACK handling, and other functionality such as APRS bulletins (supporting both static and dynamic contents) and APRS beaconing. However, ```core-aprs-client``` deliberately lacks any _specific_ APRS bot functions such as WX reporting etc. 

This is where _you_ step in. Add your bot-specific code to the client's APRS framework code. Everything else related to APRS messaging and communication with APRS-IS will be covered by the ```core-aprs-client``` framework.

## Sample APRS Client

The following example illustrates a fully functional APRS bot. You will provide the APRS message input parser code and the generator responsible for the outgoing APRS message content. Everything else will be handled by the `core-aprs-client` framework.

```python
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

import logging

if __name__ == '__main__':
    client = CoreAprsClient(config_file="core_aprs_client.cfg",
                            log_level=logging.INFO,
                            input_parser=parse_input_message,
                            output_generator=generate_output_message)
    client.activate_client()
```

It's as simple as that.

## Core features
- Core APRS-IS functionality, covering both 'old' and '[new](http://www.aprs.org/aprs11/replyacks.txt)' ACK processing
- Configurable dupe message handler
- Optional:
    - APRS beacons and bulletins, including support for dynamic bulletin content generated during runtime
    - Program crash handler, allowing you to get notified in case the client program crashes

## Installation and Configuration

### Installation instructions
Instructions for installing the framework and its sample APRS client on your computer can be found [here](docs/installation.md).

### Client Configuration
The steps for modifying the client's config file are described [here](docs/configuration.md).

### Framework examples 
[This directory](framework_examples/README.md) contains sample program code; it also contains the ready-to-use templates for the framework's configuration files.

### `CoreAprsClient` class description
The framework's class methods are described [here](docs/coreaprsclient_class.md)

### Source Code Anatomy
A brief overview on this repositories' software modules used by the client can be found [here](docs/anatomy.md).

### Framework usage
The steps for using the client framework are described [here](docs/framework_usage.md).

### Client schematics
If you want to learn about the bot's basic processing structure, then have a look at [this diagram](docs/schematics.md).

## Known issues and caveats
- This software is single-threaded. Due to APRS-IS's technical nature of resubmitting non-ack'ed messages, this limitation should not be an issue, though. Future versions of this software might support queued processing of incoming requests.
- This software is intended to be used by licensed ham radio operators. If you are not a licensed ham radio operator, then this program is not (yet) for you. Why not take a look at sites such as [Hamstudy](https://hamstudy.org/) and [50 Ohm](https://50ohm.de/) - and get licensed?
- You should at least know the APRS basics before you use this software. Acquaint yourself with [the official APRS documentation](https://github.com/wb2osz/aprsspec) and learn about [how APRS works](https://how.aprs.works/) in general. Additionally, have a look at the [APRS Foundation](https://www.aprsfoundation.org/)'s website.
- You HAVE to assign your personal call sign to the bot.
- You HAVE to [request your personal APRS TOCALL](https://github.com/aprsorg/aprs-deviceid) for using this bot __in production__. See the [APRS Device ID](https://github.com/aprsorg/aprs-deviceid/blob/main/ALLOCATING.md#development-phase) information section on proper usage.
