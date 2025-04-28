# core-aprs-client

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)




Core APRS client framework with dupe detection, bulletin/beaconing support, and other APRS-IS related stuff.

```core-aprs-client``` is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s APRS functions which can be used for building your very own APRS client / bot. Its framework supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS messaging functions, such as connecting to APRS-IS, message dupe detection, ACK/REJ handling, and other functionality such as APRS bulletins and beacons. However, ```core-aprs-client``` deliberately lacks any _specific_ APRS bot functions such as WX reporting etc. 

This is where _you_ step in. Add your bot-specific code to the client's APRS framework code. Everything else related to APRS messaging and communication with APRS-IS will be covered by the ```core-aprs-client``` framework.

## Core features
- Core APRS-IS functionality, covering both 'old' and '[new](http://www.aprs.org/aprs11/replyacks.txt)' ACK/REJ processing
- Configurable dupe message handler
- Optional:
    - Support for APRS beaconing and bulletins
    - Program crash handler, allowing you to get notified in case the client program crashes

## Installation and Configuration

### Installation instructions
Documentation on how to install the client to your computer can be found [here](docs/installation.md)

### Client Configuration
The steps for modifying the client's config file are described [here](docs/configuration.md).

### Running the client
The steps for starting the client are described [here](docs/client_start.md).

### Source Code Anatomy
A brief overview on the software modules used by the client can be found [here](docs/anatomy.md).

### Extending the client with your own bot code
The steps for adding your own extensions to the client are described [here](docs/extensions.md).

### Client schematics
If you want to learn about the bot's basic processing structure, then have a look at [this diagram](docs/schematics.md).

## Known issues and caveats
- This software is single-threaded. Due to APRS-IS's technical nature of resubmitting non-ack'ed messages, this limitation should not be an issue, though. Future versions of this software might support queued processing of incoming requests.
- This software is intended to be used by licensed ham radio operators. If you are not a licensed ham radio operator, then this program is not (yet) for you. Why not take a look at sites such as [Hamstudy](https://hamstudy.org/) and [50 Ohm](https://50ohm.de/) - and get licensed?
- You should at least know the APRS basics before you use this software. Acquaint yourself with [the official APRS documentation](https://github.com/glidernet/ogn-aprs-protocol/blob/master/APRS101.PDF) and learn about [how APRS works](https://how.aprs.works/) in general. Additionally, have a look at the [APRS Foundation](https://www.aprsfoundation.org/)'s web site.
- You HAVE to assign your personal call sign to the bot.
- You HAVE to [request your personal APRS TOCALL](https://github.com/aprsorg/aprs-deviceid) for using this bot __in production__. See the [APRS Device ID](https://github.com/aprsorg/aprs-deviceid/blob/main/ALLOCATING.md#development-phase) information section on proper usage.
- ```core_aprs_client``` uses [aprslib](https://github.com/rossengeorgiev/aprs-python) for its APRS-IS communication. As ```aprslib``` currently does not support the transfer of additional external variables to its callback function (e.g. via ```kwargs```), some of the variables that ```core-aprs-client``` needs to communicate with have been defined as globally shared variables (via `client_shared.py`). 
