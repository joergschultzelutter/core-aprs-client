# Source Code Anatomy and Usage

Brief overview of `core-aprs-client`'s source files. 

```
├── sample_aprs_client
│   ├── apprise.yml.TEMPLATE
│   ├── core_aprs_client.cfg.TEMPLATE
│   ├── input_parser.py
│   ├── output_generator.py
│   └── sample_aprs_client.py
└── src
    └── CoreAprsClient
        ├── CoreAprsClient.py
        ├── __init__.py
        ├── _version.py
        ├── client_aprs_communication.py
        ├── client_aprsobject.py
        ├── client_configuration.py
        ├── client_expdict.py
        ├── client_logger.py
        ├── client_message_counter.py
        ├── client_return_codes.py
        ├── client_shared.py
        └── client_utils.py
```

## Python package modules

Location: `~/src/CoreAprsClient`

| File Name                       | Usage                                                                                                                                                                                                                             |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_version.py`                   | Contains the framework's version number                                                                                                                                                                                           |
| `client_aprs_communication.py`  | Everything [APRS-IS](https://aprs-is.net/) related, such as sending messages and acknowledgments                                                                                                                                  |
| `client_aprsobject.py`          | Wrapper class for the [APRS-IS](https://aprs-is.net/) object, thus allowing it to be used by the callback function                                                                                                                |
| `client_configuration.py`       | Wrapper code for the client configuration data. Also takes care of type conversions (string to bool/float/int) from the original configuration data settings                                                                      |
| `client_expdict.py`             | Wrapper class for the expiring dictionary object, thus allowing it to be used by the callback function                                                                                                                            |
| `client_logger.py`              | Wrapper class for the logging object. Defines the program's logging level (such as `DEBUG`, `INFO`, ...) for the whole client. Default logging level: `INFO`. `CoreAprsClient.py`'s constructor can overwrite this default value. |
| `client_message_counter.py`     | Wrapper class for the APRS message counter object, thus allowing it to be used by the callback function                                                                                                                           |
| `client_shared.py`              | Wrapper code for all shared objects between the program's `main` class and its [APRS-IS](https://aprs-is.net/) callback code                                                                                                      |
| `client_utils.py`               | Various utility functions which are used throughout the client.                                                                                                                                                                   |
| `CoreAprsClient.py`             | Main class                                                                                                                                                                                                                        |

## Configuration files 

Location: `~/sample_aprs_client`

>[!NOTE]
>Although most of these configuration files are provided with predefined default content, you do need to modify these files.

| File Name                       | Usage                                                                                                                                                                                                                                           |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apprise.yml.TEMPLATE`          | Contains the [Apprise](https://www.github.com/caronc/apprise) configuration for `COAC`'s [crash handler](configuration_subsections/config_crash_handler.md). File name is referenced in the `core_aprs_client_cfg.TEMPLATE` configuration file. |
| `core_aprs_client_cfg.TEMPLATE` | `core-aprs-client`'s master configuration file. Rename the file (default file name is `core_aprs_client.cfg` and add your configuration data as described [here](configuration.md).                                                             |

## User files

Location: `~/sample_aprs_client`

>[!NOTE]
>These files are stubs which will help you to understand how `core-aprs-client` works. For production use, you need to modify these files.

| File Name               | Usage                                                                                                                                                                                                                                         |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `input_parser.py`       | Parses ingress APRS data and tries to understand what the APRS user wants us to do. Prepares the command data for `output_generator.py`. See [the documentation on extending](framework_usage.md) `core-aprs-client` for further information. |
| `output_generator.py`   | Takes the command data from `input_parser.py` and builds the future output message for the [APRS-IS](https://aprs-is.net/) user. See [the documentation on extending](framework_usage.md) `core-aprs-client` for further information.         |
| `sample_aprs_client.py` | APRS demo client, based on the `core-aprs_client` framework. Uses `input_parser.py` `output_generator.py` for data processing. Demonstrates online connections to [APRS-IS](https://aprs-is.net/) and offline parser testing.                 |
