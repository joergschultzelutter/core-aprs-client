# Testing

> [!TIP]
> This section of the configuration file allows you to enable internal functions that are dedicated to testing purposes only. Normally, you don't need to change any of these settings

| Config variable                   | Type      | Default value | Description                                                                                                                                                                                                                                                                                                                |
|-----------------------------------|-----------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprsis_enforce_unicode_messages` | `boolean` | `false`       | When set to `true`, the bot's egress data will allow UTF-8 messages. Additionally, `core-aprs-client` will not try to convert egress data to ASCII-7 content. Note that such messages may not be compatible with APRS transceivers.                                                                                        |
| `aprsis_simulate_send`            | `boolean` | `false`       | When set to `true`, the bot will not send _any_ data (including message ACKs) to APRS-IS. Instead, it will just _simulate_ egress data processing and output the content to `stdout`. Note that ingress messaging is not affected, meaning that you can send messages to the bot via handheld and/or APRS-IS at any time.  |

The respective section from `core-aprs-client`'s config file lists as follows:

```
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
```
