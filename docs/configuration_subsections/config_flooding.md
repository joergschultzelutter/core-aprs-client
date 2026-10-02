# APRS Flooding Prevention

> [!TIP]
> Configuration settings for the program's message flooding prevention handler. It is only effective for the live communication between APRS-IS and the bot.

This configuration section is responsible for the settings of the APRS Flooding Prevention Handler. If a user sends an invalid command to the bot, it will always respond with its standard error message.

In the worst-case scenario, where the user sends hundreds of invalid commands to the bot, it would also send hundreds of identical standard error messages to the user.

The Flooding Prevention Handler prevents this. For each standard error message, a combination of the callsign and the number of error messages sent so far is stored. When this number reaches a threshold, a different, configurable error message ([`aprs_flooding_error_message`](config_client.md)) is finally sent to the user. Any further attempts to generate an error will then be ignored by the bot up until the entry in our expiring dict has expired.

Increasing the `aprs_flooding_number_of_entries` counter will result in a timer reset of the previous entry, meaning that the previous item (now increased by a value of 1) will again live a whole `aprs_flooding_time_to_live` time span.

Please note:

- All incoming messages will still be answered with an ACK whenever possible. This will also prevent request flooding on a low protocol level.
- Valid messages will also continue to be processed. However, due to [dupe detection](config_dupe_detection.md) mechanism, sending an identical APRS message means that even such duplicates will not be answered by the bot.
- If you set `aprs_flooding_counter_reset_for_good_msgs` to `true`, any message that the bot CAN process will reset the flooding counter for that call sign to zero.

This configuration section contains four settings:

| Config variable                             | Type   | Default value | Description                                                                                                                                                                                                                                                                           |
|---------------------------------------------|--------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprs_flooding_default_error_threshold`     | `int`  | `3`           | If this number is reached by generating a default response n consecutive times, `aprs_flooding_error_message` will be used ONCE instead of `aprs_input_parser_default_error_message`. Once that threshold has been exceeded, NO default error message AT ALL is returned to the user. |
| `aprs_flooding_number_of_entries`           | `int`  | `2160`        | Expiring dictionary for flooding messages: number of entries                                                                                                                                                                                                                          |
| `aprs_flooding_time_to_live`                | `int`  | `1800`        | Expiring dictionary for flooding messages: time-to-live in seconds                                                                                                                                                                                                                    |
| `aprs_flooding_counter_reset_for_good_msgs` | `bool` | `false`       | Expiring dictionary for flooding messages: reset `aprs_flooding_default_error_threshold` counter to zero in case a positive message has been processed in between                                                                                                                     |
 


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
# If this number is reached by generating a default response n consecutive times, 
# `aprs_flooding_error_message` will be used ONCE instead of `aprs_input_parser_default_error_message`. 
# Once that threshold has been exceeded, NO default error message AT ALL is returned to the user.
aprs_flooding_default_error_threshold = 3
# 
# Expiring dictionary for flooding messages: number of entries
aprs_flooding_number_of_entries = 2160
#
# Expiring dictionary for flooding messages: time-to-live in seconds
aprs_flooding_time_to_live = 1800
#
# Expiring dictionary for flooding messages: reset `aprs_flooding_default_error_threshold` counter to zero in case a positive message has been processed in between 
aprs_flooding_counter_reset_for_good_msgs = false
#
```
