# core-aprs-client
Core APRS client with dupe detection and other stuff.

```core-aprs-client``` is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s APRS functions which can be used for building your very own APRS client / bot. It supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS messaging functions, such as connecting to APRS-IS, message dupe detection, ACK/REJ handling, and other functionality. Hoewever, ```core-aprs-client``` deliberately lacks functions such as WX reporting etc. 

This is where you can step in. Just add your bot-specific code to the client and you're literally done. Everything related to APRS messaging and communication with APRS-IS will be covered by ```core-aprs-client```.

## Core features
- Core APRS-IS functionality, covering both 'old' and '[new](http://www.aprs.org/aprs11/replyacks.txt)' ACK/REJ processing
- Configurable dupe message handler
- APRS Beaconing and Bulletins (optional)
- Program crash handler, allowing you to get notified in case the client crashes (optional)

## Configuring the client
The steps for starting the client are described [here](docs/configuration.md).

## Running the client
The steps for starting the client are described [here](docs/client_start.md).

## Extending the client
The steps for adding your own extensions to the client are described [here](docs/extensions.md).

## Client schematics
If you want to learn about the bot's basic structure, then have a look at [this diagram](docs/schematics.md).

## Known issues
- This software is single-threaded. Due to APRS-IS's technical nature of resubmitting non-ack'ed messages, this should not be an issue, though.
- If you are not a licensed ham radio operator, then this program is not for you. Additionally, you should at least know the APRS basics before you use this code.
- You HAVE to assign your personal call sign to the bot.
- You HAVE to request your personal APRS TOCALL for using this bot.
