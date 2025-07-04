# Program Configuration File

When it comes to the user's individual configuration settings, `core-aprs-client` solely relies on an external config file. Its default file name is `core-aprs-client.cfg` and can be overwritten by specifying an individual file name program parameter during program start.

`core-aprs-client.cfg` is divided into multiple sections whose contents will be described in the following help pages. Each documentation page contains the associated configuration variables along with their data types (`str`, `int`, `float`, and `boolean`). Note that `boolean` value settings in the configuration file are case-insensitive and provide support for custom key values:

| Setting in config file  | Python `bool` equivalent |
|-------------------------|--------------------------|
| `true`, `yes`, or `on`  | `True`                   |
| `false`, `no`, or `off` | `False`                  |

> [!NOTE]
> Except for the first two configuration sections, all other configuration sections are _optional_ and have been pre-configured. If you are happy with the default settings, modify those parts of the config file which _do_ require modifications (e.g. call sign, passcode) — and you're good to go.


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





