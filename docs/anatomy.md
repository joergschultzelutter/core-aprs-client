# Source Code Anatomy and Usage

Brief overview of `core-aprs-client`'s source files. 

## Python package modules

Location: `~/src/CoreAprsClient`

| File Name                       | Usage                                                                                                                                                                                                                                                  |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_version.py`                   | Contains the program's version number                                                                                                                                                                                                                  |
| `client_aprs_communication.py`  | Everything APRS-IS related, such as sending messages and acknowledgments                                                                                                                                                                               |
| `client_aprsobject.py`          | Wrapper class for the APRS-IS object, thus allowing it to be used by the callback function                                                                                                                                                             |
| `client_configuration.py`       | Wrapper code for the client configuration data. Also takes care of type conversions (string to bool/float/int) from the original configuration data settings                                                                                           |
| `client_expdict.py`             | Wrapper class for the expiring dictionary object, thus allowing it to be used by the callback function                                                                                                                                                 |
| `client_logger.py`              | Wrapper class for the logging object. Defines the program's logging level (such as `DEBUG`, `INFO`, ...) for the whole client. Default logging level: `INFO`. Change this setting to `DEBUG` if you want to see more output in the program's log file. |
| `client_message_counter.py`     | Wrapper class for the APRS message counter object, thus allowing it to be used by the callback function                                                                                                                                                |
| `client_shared.py`              | Wrapper code for all shared objects between the program's `main` class and its APRS-IS callback code                                                                                                                                                   |
| `client_utils.py`               | Various utility functions which are used throughout the client.                                                                                                                                                                                        |
| `CoreAprsClient.py`             | Main class                                                                                                                                                                                                                                             |

## Configuration files 

>[!NOTE]
>Although most of these configuration files are provided with predefined default content, you do need to modify these files.

| File Name                       | Usage                                                                                                                                                                                                                                                  |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apprise.yml.TEMPLATE`          | Contains the [Apprise](https://www.github.com/caronc/apprise) configuration for `COAC`'s [crash handler](configuration_subsections/config_crash_handler.md)                                                                                            |
| `core_aprs_client_cfg.TEMPLATE` | The program's config file. Rename the file (default file name is `core_aprs_client.cfg` and add your configuration data as described [here](configuration.md).                                                                                         |

## User files

>[!NOTE]
>These files are stubs which will help you to understand how `core-aprs-client` works. For production use, you need to modify these files.

| File Name                       | Usage                                                                                                                                                                                                                                                  |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `client_input_parser.py`        | Parses ingress APRS data and tries to understand what the APRS user wants us to do. Prepares the command data for `client_output_generator.py`. See [the documentation on extending](extensions.md) `COAC` for further information.                    |
| `client_output_generator.py`    | Takes the command data from `client_input_parser.py` and builds the future output message for the APRS-IS user. See [the documentation on extending](extensions.md) `COAC` for further information.                                                    |
