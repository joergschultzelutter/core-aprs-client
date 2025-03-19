# core-aprs-client
Core APRS client with dupe detection

This is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS functions which can be used for building your very own APRS client / bot. It supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS functions, such as connecting to APRS-IS, message dupe detection, ACK/REJ handling, and other functionality. You are then required to add a proper input parser and then generate message content that is to be sent to the user. Everything critical to APRS will be covered by the core-aprs-client.

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