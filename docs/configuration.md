# Program Configuration File

When it comes to the individual configuration, the```core-aprs-client``` solely relies on an external config file. The default file name is ```core-aprs-client.cfg``` and can be overwritten by specifying an individual file name program parameter during program start.

```core-aprs-client.cfg``` is divided into multiple sections whose contents will be described in the following help pages. 

> [!NOTE]
> With the exception of the first two configuration sections, all other configuration sections are optional and have been pre-configured. If you are happy with the default settings, simply modify those parts of the config file which _do_ require modifications (e.g. call sign, passcode) - and you're good to go.

## Mandatory configuration file sections

- [client_config](configuration/config_client.md) - Basic APRS call sign & filter configuration.
- [network_config](configuration/config_network.md) - APRS-IS networking settings, such as server, port, passcode,....

## Optional configuration file sections

- [beacon_data](configuration/config_beacon.md) - Used in case you want to beacon your APRS bot's position & APRS symbol to APRS-IS
- [bulletin_data](configuration/config_bulletin.md) - Used in case you want to send out fixed APRS bulletin messages to APRS-IS
- [crash_handler](configuration/config_crash_handler.md) - Optional setting which enables the bot to send you a core dump file in case the program has crashed.
- [dupe_detection](configuration/config_dupe_detection.md) - Default settings for how many incoming APRS messages are stored. The time-to-live setting can also be defined here.
- [message_delay](configuration/config_message_delay.md) - Can be used for configuring the delays between outgoing multiple APRS-IS messages
- [testing](configuration/config_testing.md) - Configuration settings for software and integration testing
- [custom_config](configuration/config_custom.md) - Empty. You can store your very own configuration settings in this section; ```core-aprs-client``` will then make these available to you





