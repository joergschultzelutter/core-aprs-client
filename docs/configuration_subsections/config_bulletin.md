# Bulletin Configuration & Data

> [!TIP]
> This section of the configuration file allows you to enable APRS bulletin broadcasting. APRS supports so-called "bulletins". All bulletins start with a "BLN" prefix and consist of up to nine (9) characters and digits. Bulletins can be used for broadcasting static or dynamic texts to _all_ APRS users. Bulletin messages are received by nearby APRS-capable transceivers and [can be viewed on aprs.fi](https://aprs.fi/bulletin/).

By default, the APRS bulletin data function is disabled (```aprsis_broadcast_bulletins = false```), meaning that ```core-aprs-client``` will not broadcast any APRS bulletins for you. If you change this setting to ```true```, then ```core-aprs-client``` will broadcast all _populated_ bulletin entries (```bln0``` to ```bln9```) in the configuration file with a fixed broadcasting interval of 4 hours.

> [!TIP]
> This section of the configuration file only configures whether bulletin messaging is switched on or off. The actual bulletin data (aka the messages that you intend to broadcast) are configured in the ```bulletin_messages``` configuration file section.

- ```aprsis_broadcast_bulletins``` - Enable or disable bulletins. Default value: ```false``` (bulletin broadcasting is disabled)
- ```aprsis_bulletin_interval_minutes``` - the interval in minutes that ```core-aprs-client``` will use for bradcasting. Default value: 240 minutes (4 hours). 
```

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
```
