# Source Code Anatomy and Usage

Brief overview of `core-aprs-client`'s source files. 

```
├── framework_examples
│   ├── apprise.yml.TEMPLATE
│   ├── core_aprs_client.cfg.TEMPLATE
│   ├── demo_aprs_client.py
│   ├── demo_aprs_client_with_dynamic_bulletins.py
│   ├── demo_dryrun.py
│   ├── input_parser.py
│   └── output_generator.py
│   └── post_processor.py
└── src
    └── CoreAprsClient
        ├── CoreAprsClient.py
        ├── __init__.py
        ├── _version.py
        ├── client_aprs_communication.py
        ├── client_aprsobject.py
        ├── client_configuration.py
        ├── client_configuration_schema.py
        ├── client_expdict.py
        ├── client_logger.py
        ├── client_message_counter.py
        ├── client_return_codes.py
        ├── client_shared.py
        └── client_utils.py
```

## Python package modules

Location: `~/src/CoreAprsClient`

| File Name                        | Usage                                                                                                                                                                                                                             |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_version.py`                    | Contains the framework's version number                                                                                                                                                                                           |
| `client_aprs_communication.py`   | Everything [APRS-IS](https://aprs-is.net/) related, such as sending messages and acknowledgments                                                                                                                                  |
| `client_aprsobject.py`           | Wrapper class for the [APRS-IS](https://aprs-is.net/) object, thus allowing it to be used by the callback function                                                                                                                |
| `client_configuration.py`        | Wrapper code for the client configuration data. Also takes care of type conversions (string to bool/float/int) from the original configuration data settings                                                                      |
| `client_configuration_schema.py` | Configuration file schema definition. Used by `client_configuration.py` in order to perform a generic validation of `core-aprs-client`'s configuration file (missing values, incorrect value types, ...)                          |
| `client_expdict.py`              | Wrapper class for the expiring dictionary object, thus allowing it to be used by the callback function                                                                                                                            |
| `client_logger.py`               | Wrapper class for the logging object. Defines the program's logging level (such as `DEBUG`, `INFO`, ...) for the whole client. Default logging level: `INFO`. `CoreAprsClient.py`'s constructor can overwrite this default value. |
| `client_message_counter.py`      | Wrapper class for the APRS message counter object, thus allowing it to be used by the callback function                                                                                                                           |
| `client_shared.py`               | Wrapper code for all shared objects between the program's `main` class and its [APRS-IS](https://aprs-is.net/) callback code                                                                                                      |
| `client_utils.py`                | Various utility functions which are used throughout the client.                                                                                                                                                                   |
| `CoreAprsClient.py`              | Main class                                                                                                                                                                                                                        |

## Configuration files 

Location: `~/framework_examples`

>[!NOTE]
>Although most of these configuration files are provided with predefined default content, you do need to modify these files.

| File Name                       | Usage                                                                                                                                                                                                                                           |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `apprise.yml.TEMPLATE`          | Contains the [Apprise](https://www.github.com/caronc/apprise) configuration for `COAC`'s [crash handler](configuration_subsections/config_crash_handler.md). File name is referenced in the `core_aprs_client_cfg.TEMPLATE` configuration file. |
| `core_aprs_client_cfg.TEMPLATE` | `core-aprs-client`'s master configuration file. Rename the file (default file name is `core_aprs_client.cfg` and add your configuration data as described [here](configuration.md).                                                             |

## User files

Location: `~/framework_examples`

>[!NOTE]
>These files are stubs which will help you to understand how `core-aprs-client` works. For production use, you need to modify these files.

| File Name                                    | Usage                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `input_parser.py`                            | Parses ingress APRS data and tries to understand what the APRS user wants us to do. Prepares the command data for `output_generator.py`. See [the documentation on extending](/docs/framework_usage.md#extending-the-input-parser-input_parserpy) `core-aprs-client` for further information.                                                                                                                                                      |
| `output_generator.py`                        | Takes the command data from `input_parser.py` and builds the future output message for the [APRS-IS](https://aprs-is.net/) user. See [the documentation on extending](/docs/framework_usage.md#extending-the-output-generator-output_generatorpy) `core-aprs-client` for further information.                                                                                                                                                      |
| `post_processor.py`                          | Optional. Takes the post processing output data from `output_generator.py`. If the user has assigned a post processing function to the class' instance AND post processing data is present, that post processing function is executed AFTER the APRS response has been sent to the user.  See [the documentation on extending](/docs/framework_usage.md#extending-the-post-processor-post_processorpy) `core-aprs-client` for further information. |
| `demo_aprs_client.py`                        | APRS demo client, based on the `core-aprs_client` framework. Uses `input_parser.py` `output_generator.py` for data processing. Demonstrates online connections to [APRS-IS](https://aprs-is.net/) and offline parser testing.                                                                                                                                                                                                                      |
| `demo_aprs_client_with_dynamic_bulletins.py` | Same as `demo_aprs_client.py`, but with a demonstration of [dynamic bulletins support](coreaprsclient_class.md#use-of-dynamic-content-for-aprs-bulletins-additional-to-static-bulletin-content)                                                                                                                                                                                                                                                    |
| `demo_dryrun.py`                             | Demonstrates `core-aprs_client`'s ['dryrun'](coreaprsclient_class.md#dryrun_testcall-class-method) functionality.                                                                                                                                                                                                                                                                                                                                  |
| `demo_print_config_data.py`                  | Demonstrates `core-aprs_client`'s option of configuration data retrieval by using the class' 'getter' method.                                                                                                                                                                                                                                                                                                                                      |
