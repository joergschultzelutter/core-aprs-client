# Testing

> [!TIP]
> This section of the configuration file allows you to enable internal functions that are dedicated to testing purposes only. Normally, you don't need to change any of these settings

- ```aprsis_enforce_unicode_messages``` (default: ```false```) When set to ```true```, the bot's egress data will allow UTF-8 messages. Additionally, ```core-aprs-client``` will not try to convert egress data to ASCII-7 content. Note that such messages may not be compatible with APRS transceivers. 
- ```aprsis_simulate_send``` (default: ```false```) When set to ```true```, the bot will not send data to APRS-IS. Instead, it will just simulate egress data processing. Note that ingress messages sent to the bot are regularly digested.



```
[testing]
#
# Force outgoing unicode messages (default: false)
# When set to 'true', outgoing content will allow UTF-8 encoding
# Enabling this setting is only recommended for APRS-IS-to-APRS-IS testing
aprsis_enforce_unicode_messages = false
#
# Simulates sending to APRS only, if set to true
# (useful for initial testing purposes only)
# Default: false
aprsis_simulate_send = false
```
