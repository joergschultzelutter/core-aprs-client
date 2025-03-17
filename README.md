# core-aprs-client
Core APRS client with dupe detection

This is a modernized version of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS functions which can be used for building your very own APRS client / bot. It supports all of [mpad](https://github.com/joergschultzelutter/mpad)'s core APRS functions, such as connecting to APRS-IS, message dupe detection, ACK/REJ handling, and other functionality. You are then required to add a proper input parser and then generate message content that is to be sent to the user. Everything critical to APRS will be covered by the core-aprs-client.

## Configuration
This repository comes with a configuration file template which can be used for amending your program instance. Rename the file called ``core_aprs_client.cfg.TEMPLATE`` to ``core_aprs_client.cfg`` (default config file name; you can choose a different one) and amend the settings:

```
[config]

# This is the configuration file for the Core APRS Client
# Refer to the program documentation at https://github.com/joergschultzelutter/core-aprs-client
# for additional information on what these settings do

#
# BEGIN of APRS call sign configuration settings
#
# APRS Listener call sign
# Default call sign is COAC (*CO*re *A*prs *C*lient)
# Change BOTH aprsis_callsign and aprsis_server_filter settings
# in case you want to use a different call sign
#
# This is the call sign on which the APRS client listens to
# while being connected to APRS-IS. Read: you have to send
# your messages to this call sign
aprsis_callsign = COAC
#
# APRS-IS message filter settings - see https://www.aprs-is.net/javAPRSFilter.aspx
# Usually, you don't want to change the filter setting. Just ensure that both
# aprsis_callsign and aprsis_server_filter relate to the same call sign!
aprsis_server_filter = g/COAC
#
# This is the APRS "tocall" identifier that is used for outgoing messages
# You NEED to request your very own TOCALL for your code
# Details: https://github.com/aprsorg/aprs-deviceid
aprsis_tocall = APRS
#
# END of call sign configuration settings
#
# Standard APRS client parameters. Amend if necessary.
#
# APRS-IS server, see https://www.aprs2.net/
aprsis_server_name = euro.aprs2.net
#
# APRS-IS port number, see https://www.aprs-is.net/connecting.aspx
# Usually, you don't want to change this
aprsis_server_port = 14580
#
# Simulates sending to APRS only, if set to true
# (useful for initial testing purposes only)
# Default: false
aprsis_simulate_send = false
#
# APRS-IS passcode (numeric). Replace with your very own passcode
# If you don't know what this is, then this program is not for you
aprsis_passcode = 29166

# Internal dupe message cache configuration
#
# maximum number of messages
msg_cache_max_entries = 2160
#
# max time span of dupe detection (3600 sec = 1 hour)
msg_cache_time_to_live = 3600
#
# delay between messages if more than one message is to be sent to APRS-IS
packet_delay_message = 6.0
#
# packet delay after sending an acknowledgment, bulletin or beacon
packet_delay_other = 6.0
#
# Broadcast position true/false
# if set to 'true', the client will beacon its existence plus lat/lon settings
# every 4 hrs
aprsis_broadcast_position = false
#
# Symbol for position broadcasting
# (only used for cases where aprsis_broadcast_position = true)
# see http://www.aprs.org/symbols/symbolsX.txt
# table: APRS symbol table (/=primary \=secondary, or overlay)
# symbol: APRS symbol: Server
aprsis_table = /
aprsis_symbol = ?
#
# Latitude and longitude
# (only used for cases where aprsis_broadcast_position = true)
# Location of our process (Details: see aprs101.pdf see aprs101.pdf chapter 6 pg. 23)
# Ensure to honor the format settings as described in the specification, otherwise
# your package might get rejected and/or not surface on aprs.fi
# Degrees: lat: 0-90, lon: 0-180
# Minutes and Seconds: 00-60
# Bearing: latitude N or S, longitude: E or W
# latitude=8 chars fixed length, ddmm.ssN
# longitude = 9 chars fixed length, dddmm.ssE
aprsis_latitude = 5151.84N
aprsis_longitude = 00935.48E
#
# Altitude in *FEET* (not meters) for APRS beacon. Details: see aprs101.pdf chapter 8
# (only used for cases where aprsis_broadcast_position = true)
aprsis_beacon_altitude_ft = 824
#
#
# Broadcast APRS bulletins (BLN0..9) true/false
# if set to 'true', the client will beacon a FIXED set of APRS bulletin messages
# every 4 hrs. The messages are defined in the 'core_aprs_client.py' file
#
aprsis_broadcast_bulletins = false
#
# Apprise config file name
# Reference to an Apprise (https://github.com/caronc/apprise) configuration file
# If value is set to NOT_CONFIGURED, Apprise messaging will be ignored
apprise_config_file = apprise.yml
#
# file name of the "nohup" file
# When you start the client, you will run something like
#
# nohup python core_aprs_client.py >nohup.out &
#
# If the apprise config is enabled AND you have specified a correct file name
# for this setting, the client will try to message you a potential call stack file
# in case the program crashes
nohup_filename="nohup.out"
#
# Force outgoing unicode messages (default: false)
# When set to 'true', outgoing content will allow UTF-8 encoding
# Enabling this setting is only recommended for APRS-IS-to-APRS-IS testing
aprsis_enforce_unicode_messages = false
```

## Running the client

Almost every configuration setting is stored in the program's config file - see previous chapter

```
usage: core_aprs_client.py [-h] [--configfile CONFIGFILE]

options:
  -h, --help                show this help message and exit
  --configfile CONFIGFILE   Program config file name (default is 'core_aprs_client.cfg')
```
 Run the program via ``nohup python core_aprs_client.py >nohup.out &``