# Program Configuration File

When it comes to the user's individual configuration settings, `core-aprs-client` solely relies on an external config file. Its default file name is `core-aprs-client.cfg` and can be overwritten by specifying an individual file name program parameter during program start.

`core-aprs-client.cfg` is divided into multiple sections whose contents will be described in the following help pages. Each documentation page contains the associated configuration variables along with their data types (`str`, `int`, `float`, and `boolean`). Note that `boolean` value settings in the configuration file are case-insensitive and provide support for custom key values:

| Setting in config file  | Python `bool` equivalent |
|-------------------------|--------------------------|
| `true`, `yes`, or `on`  | `True`                   |
| `false`, `no`, or `off` | `False`                  |

> [!NOTE]
> Except for the first two configuration sections, all other configuration sections are _optional_ and have been pre-configured. If you are happy with the default settings, modify those parts of the config file which _do_ require modifications (e.g. call sign, passcode) — and you're good to go.

> [!TIP]
> Complete sample file templates for both the configuration file and the Apprise configuration file can be found in the `sample_aprs_client` directory.

## Mandatory configuration file sections

| Configuration Section                                         | Usage                                                                           |
|---------------------------------------------------------------|---------------------------------------------------------------------------------|
| [client_config](configuration_subsections/config_client.md)   | Basic APRS call sign & filter configuration.                                    |
| [network_config](configuration_subsections/config_network.md) | APRS-IS networking settings, such as server, port, passcode, and APRS-IS filter |

## Optional configuration file sections

> [!Tip]
> These configuration file sections have been preconfigured. You can use the file's default settings unless you want to use a very specific configuration for your program's purposes.

| Configuration Section                                                                                                                            | Usage                                                                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| [beacon_config](configuration_subsections/config_beacon.md)                                                                                      | Used in case you want to beacon your APRS bot's position & APRS symbol to APRS-IS                                                   |
| [bulletin_config](configuration_subsections/config_bulletin.md) and [bulletin_messages](configuration_subsections/config_bulletin_messages.md)   | Used in case you want to send out fixed APRS bulletin messages to APRS-IS                                                           |
| [crash_handler](configuration_subsections/config_crash_handler.md)                                                                               | Optional setting which enables the bot to send you a core dump file in case the program has crashed.                                |
| [dupe_detection](configuration_subsections/config_dupe_detection.md)                                                                             | Default settings for how many incoming APRS messages are stored. The time-to-live setting can also be defined here.                 |
| [message_delay](configuration_subsections/config_message_delay.md)                                                                               | Configures the delays between outgoing multiple APRS-IS messages                                                                    |
| [testing](configuration_subsections/config_testing.md)                                                                                           | Configuration settings for software and integration testing                                                                         |
| [data_storage](configuration_subsections/config_data_storage.md)                                                                                 | Configuration settings for the storage of data files, e.g. the data file which persists the APRS message counter                    |
| [custom_config](configuration_subsections/config_custom.md)                                                                                      | Empty. You can store your very own configuration settings in this section; `core-aprs-client` will then make these available to you |

## Configuration file sample

```
# Core APRS Client (COAC) configuration file
# Refer to the program documentation at
# https://github.com/joergschultzelutter/core-aprs-client/blob/master/docs/configuration.md
# for additional information on what these settings do

[client_config]
#
# APRS Listener call sign. Default call sign is COAC
# This is the call sign on which the APRS client listens to
# while being connected to APRS-IS. Read: you have to send
# your messages to this call sign
# Change BOTH aprsis_callsign and aprsis_server_filter settings
# in case you want to use a different call sign
aprsis_callsign = COAC
#
# This is the APRS "tocall" identifier which is used for outgoing messages
# You NEED to request your very own TOCALL for your own client code
# Details: https://github.com/aprsorg/aprs-deviceid
aprsis_tocall = APRS
#
# This variable is used by the Apprise communication subroutines
# Its contents are freely configurable and will be used in case
# of program crashes (e.g. Telegram messages to the bot's host)
aprs_client_name = Core APRS Client
#
# This is the bot's default error message. It will be sent to the user
# whenever the input parser was unable to understand the user's message.
aprs_input_parser_default_error_message = Did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client
#
# Enable or disable message enumeration.
# message enumeration = True:  add trailing two-digit message number to the
#                              end of each message. Content for the max msg
#                              len gets reduced to 59 characters (excluding
#                              message number)
# message enumeration = False: do not add trailing message number to the end
#                              of each message. Message len stays at 67 chars
#
# Default setting: message enumeration = False
aprs_message_enumeration = False

[network_config]
#
# APRS-IS server, see https://www.aprs2.net/
aprsis_server_name = euro.aprs2.net
#
# APRS-IS port number, see https://www.aprs-is.net/connecting.aspx
# Usually, you don't want to change this
aprsis_server_port = 14580
#
# APRS-IS passcode (numeric). Replace with your very own passcode
# If you don't know what this is, then this program is not for you
aprsis_passcode = 12345
#
# APRS-IS message filter settings - see https://www.aprs-is.net/javAPRSFilter.aspx
# Ensure that both aprsis_callsign and aprsis_server_filter relate to the same call sign!
aprsis_server_filter = g/COAC

[beacon_config]
#
# Broadcast position beacon true/false
# When set to 'true', the client will beacon its existence plus lat/lon settings
# every 4 hrs
# When set to 'false', all other parameters in this section are going to be ignored
#
aprsis_broadcast_beacon = false
#
# Symbol for position broadcasting
# (only used for cases where aprsis_broadcast_beacon = true)
# see http://www.aprs.org/symbols/symbolsX.txt
# table: APRS symbol table (/=primary \=secondary, or overlay)
# symbol: APRS symbol: Server
aprsis_table = /
aprsis_symbol = ?
#
# Latitude and longitude
# (only used for cases where aprsis_broadcast_beacon = true)
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
# (only used for cases where aprsis_broadcast_beacon = true)
aprsis_beacon_altitude_ft = 824
#
#
# Broadcast interval for beacons (default: 30 minutes)
aprsis_beacon_interval_minutes = 30

[bulletin_config]
#
# Broadcast APRS bulletins (e.g. BLN0..9) true/false
# When set to 'true', the client will beacon a FIXED set of APRS bulletin messages
# every 4 hrs.
# When set to 'false', all other parameters in this section are going to be ignored
aprsis_broadcast_bulletins = false
#
# Broadcast interval for bulletins (default: 240 minutes = 4 hours)
aprsis_bulletin_interval_minutes = 240


[bulletin_messages]
#
# APRS Bulletin messages BLN0..BLN9
# If you don't want to configure a bulletin message, then leave the value empty or
# remove the line in question
#
# Notes:
# - The variable name used in this section will be used for broadcasting, meaning that if you create a variable `blnhello`, the `core-aprs-client` will broadcast a bulletin `BLNHELLO` along with its associated message to the APRS users.
# - The variable name always gets converted to uppercase characters; there is no need for you to use uppercase values in the configuration file.
# - All bulletin messages' variable names MUST start with the `BLN` prefix.
# - Following that fixed prefix, a combination of 6 more digits or ASCII-7 characters are permissable (0..9, A..Z)
# - Duplicate key entries (e.g. `bln0` occurs more than once) will cause a program error.
# - Message content longer than 67 characters will get truncated
# - Bullets use ASCII-7 character set only
# - Entries with no message content will be ignored and not broadcasted to APRS-IS
#
bln0 = Core APRS Client (Testing)
bln1 = See https://github.com/joergschultzelutter for
bln2 = program source code. 73 de DF1JSL
bln4 =
bln5 =
bln6 =
bln7 =
bln8 =
bln9 =

[crash_handler]
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
nohup_filename = nohup.out

[dupe_detection]
#
# Internal dupe message cache configuration
#
# maximum number of messages
msg_cache_max_entries = 2160
#
# max time span of dupe detection in seconds (3600 sec = 1 hour)
msg_cache_time_to_live = 3600

[message_delay]
#
# delay between messages if more than one message is to be sent to APRS-IS
# Unit of measure: seconds
packet_delay_message = 6.0
#
# packet delay after sending an ackknowledgment
# Unit of measure: seconds
packet_delay_ack = 2.0
#
# packet delay after sending the very last message from a message queue
# applies to regular messages, beacons and bulletins and is used as a grace
# period for not hitting APRS-IS messages too fast after processing a user's
# APRS request
# Unit of measure: seconds
packet_delay_grace_period = 1.0
#
# packet delay after sending a bulletin to APRS-IS and there are still pending
# bulletins in our outgoing message list
# Unit of measure: seconds
packet_delay_bulletin = 6.0
#
# packet delay after sending a beacon to APRS-IS and there are still pending
# bulletins in our outgoing message list
# Unit of measure: seconds
packet_delay_beacon = 6.0

[testing]
#
# Force outgoing unicode messages (default: false)
# When set to 'true', outgoing content will allow UTF-8 encoding
# When set to 'false', outgoing content will get downconverted to ASCII 7bit
# Enabling this setting is only recommended for APRS-IS-to-APRS-IS testing
aprsis_enforce_unicode_messages = false
#
# Simulates sending to APRS only, if set to true
# (useful for initial testing purposes only)
# Default: false
#
# false: receive AND SEND between program and APRS-IS
# true: receive from APRS-IS, but don't send anything to APRS-IS
aprsis_simulate_send = false

[data_storage]
#
# This is the name of the subdiectory where the program will store the
# APRS message counter file. Location: $cwd/<directory>
# If not present, then the directory will be created by the program
aprs_data_directory = data_files
#
# This is the name of the file that will contain the program's message counter
# If not present, then the file will be created by the program
aprs_message_counter_file_name = core_aprs_client_message_counter.txt

[custom_config]
#
# This section is deliberately kept empty and can be used for storing your
# individual APRS bot's configuration settings
```



