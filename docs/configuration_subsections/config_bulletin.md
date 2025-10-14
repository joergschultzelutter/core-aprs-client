# Bulletin Configuration

> [!TIP]
> This section of the configuration file allows you to enable APRS bulletin broadcasting. APRS supports so-called "bulletins". All bulletins start with a "BLN" prefix and consist of up to nine (9) characters and digits. Bulletins can be used for broadcasting static or dynamic texts to _all_ APRS users. Bulletin messages are received by nearby APRS-capable transceivers and [can be viewed on aprs.fi](https://aprs.fi/bulletin/).

By default, the APRS bulletin data function is disabled (`aprsis_broadcast_bulletins` = `false`), meaning that `core-aprs-client` will not broadcast any APRS bulletins for you. If you change this setting to `true`, then `core-aprs-client` will broadcast all _populated_ [bulletin_messages](config_bulletin_messages.md) from the configuration file in the given interval.

> [!TIP]
> This section of the configuration file only configures whether bulletin messaging is switched on or off. The actual bulletin data (aka the messages that you intend to broadcast) are configured in the ```bulletin_messages``` configuration file section.

| Config variable                     | Type      | Default value                  | Description                                                                                                                                                                                                            |
|-------------------------------------|-----------|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprsis_broadcast_bulletins`        | `boolean` | `false`                        | Global switch for disabling / enabling APRS bulletins. If set to `false`, all other following parameters INCLUDING the content from [bulletin_messages](config_bulletin_messages.md) are not taken into consideration. |
| `aprsis_bulletin_interval_minutes`  | `int`     | `240` (240 minutes / 4 hours)  | Defines the interval in minutes that `core-aprs-client` will use for bradcasting.                                                                                                                                      |

The respective section from `core-aprs-client`'s config file lists as follows:

```
[coac_bulletin_config]
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
