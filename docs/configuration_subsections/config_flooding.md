# APRS Flooding Prevention

> [!TIP]
> Configuration settings for the program's message flooding prevention handler. 

This configuration section is responsible for the settings of the APRS Flooding Prevention Handler. If a user sends an invalid command to the bot, it will always respond with its standard error message.

In the worst-case scenario, where the user sends hundreds of invalid commands to the bot, it would also send hundreds of identical standard error messages to the user.

The Flooding Prevention Handler prevents this. For each standard error message, a combination of the callsign and the number of error messages sent so far is stored. When this number reaches a threshold, a different, configurable error message ([`aprs_flooding_error_message`](config_client.md)) is finally sent to the user. Any further attempts to generate an error will then be ignored by the bot up until the entry in our expiring dict has expired.

Please note:

- Incoming messages will still be answered with an ACK whenever possible.
- Valid messages will also continue to be processed.

This configuration section contains three settings:

| Config variable                        | Type  | Default value | Description                                                                                                                                                           |
|----------------------------------------|-------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprs_flooding_default_error_messages` | `int` | `3`           | Number of standard error messages before a different notification is sent to the client and the bot then no longer sends error messages for a certain period of time. |
| `aprs_flooding_number_of_entries`      | `int` | `2160`        | Expiring dictionary for flooding messages: number of entries                                                                                                          |
| `aprs_flooding_time_to_live`           | `int` | `1800`        | Expiring dictionary for flooding messages: time-to-live in seconds                                                                                                    |


The respective section from `core-aprs-client`'s config file lists as follows:

```
[coac_flooding_prevention]
#
# Message anti-flooding handler
# This section limits the number of responses from the Core APRS client
# if the user has sent multiple failed requests to the bot. Once the
# threshold is reached, the user receives a final notification that no
# further error messages will be sent by the bot. Valid bot
# commands, however, will continue to be processed.
#
# Number of standard error messages before a different notification is
# sent to the client and the bot then no longer sends error messages for
# a certain period of time.
aprs_flooding_default_error_messages = 3
# 
# Expiring dictionary for flooding messages: number of entries
aprs_flooding_number_of_entries = 2160
#
# Expiring dictionary for flooding messages: time-to-live in seconds
aprs_flooding_time_to_live = 1800
```
