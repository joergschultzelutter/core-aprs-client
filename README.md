# core-aprs-client
Core APRS client with dupe detection

```core-aprs-client``` is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s APRS functions which can be used for building your very own APRS client / bot. It supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS messaging functions, such as connecting to APRS-IS, message dupe detection, ACK/REJ handling, and other functionality - but lacks specific functions such as WX reporting or other stuff that you want to use the bot for. 

This is where you will step in. Just add your bot-specific code to the client and you're done. Everything else related to APRS messaging will be covered by ```core-aprs-client```.

## Core features
- Core APRS-IS functionality, covering both 'old' and [new](http://www.aprs.org/aprs11/replyacks.txt) ACK/REJ processing
- Configurable dupe message handler
- APRS Beaconing and Bulletins (optional)
- Program crash handler, allowing you to get notified in case the client crashes (optional)

## Schematics
![Schematics](img/schematics.svg)

## Running the client

Every configuration setting is stored in the program's config file - see previous chapter. Therefore, the only command line option that can be specified is the name of the configuration file.

```
usage: core_aprs_client.py [-h] [--configfile CONFIGFILE]

options:
  -h, --help                show this help message and exit
  --configfile CONFIGFILE   Program config file name (default is 'core_aprs_client.cfg')
```
 Run the program via ``nohup python core_aprs_client.py >nohup.out &``
