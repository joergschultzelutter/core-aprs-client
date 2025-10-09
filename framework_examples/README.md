# Framework examples:

This directory contains:

## Configuration file templates

| File Name                                                      | Description                                                                                       |
|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
 | [core_aprs_client.cfg.TEMPLATE](core_aprs_client.cfg.TEMPLATE) | The framework's [configuration file](/docs/configuration.md)                                      |
 | [apprise.yml.TEMPLATE](apprise.yml.TEMPLATE)                   | The [crash handler's](/docs/configuration_subsections/config_crash_handler.md) configuration file |                                                                               

## Input parser / Output generator stubs

The provided stubs are provided for demonstration purposes only. You are required to enhance this code. For details, follow [these instructions](/docs/framework_usage.md). Both files are used by the provided `demo_..` clients in this directory

| File Name                                    | Description                                                                                                                                                   |
|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
 | [`input_parser.py`](input_parser.py)         | Takes an incoming APRS message and tries to determine what the user wants us to do. Generates the input data for [`output_generator.py`](output_generator.py) |
 | [`output_generator.py`](output_generator.py) | Takes the data from [`input_parser.py`](input_parser.py) and generates the content for the future outgoing APRS message(s).                                   |

## Demo clients

Demo clients, illustrating the framework's various use cases.

| File Name                                                                                | Description                                                                                                                                                                                                                                            |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [demo_dryrun.py](demo_dryrun.py)                                                         | Demo code which illustrates the framework's [dryrun_testcall](/docs/coreaprsclient_class.md#dryrun_testcall-class-method) method. Performs an offline parsing of a given APRS message and returns the results to the user. No interaction with APRS-IS | 
| [demo_aprs_client.py](demo_aprs_client.py)                                               | Demo code connects to APRS-IS via the framework's [activate_client](/docs/coreaprsclient_class.md#activate_client-class-method) method and acts as an APRS bot                                                                                         |
| [demo_aprs_client_with_dynamic_bulletins.py](demo_aprs_client_with_dynamic_bulletins.py) | Same as [demo_aprs_client.py](demo_aprs_client.py). In addition, dynamic bulletin data is generated and forwarded to the `core-aprs-client` framework.                                                                                                 |
| [requirements.txt](requirements.txt)                                                     | Python requirements file for the demo code                                                                                                                                                                                                             | 
> [!CAUTION]
> With its provided default execution interval settings, [demo_aprs_client_with_dynamic_bulletins.py](demo_aprs_client_with_dynamic_bulletins.py) should only be run with __disabled__ network access to APRS-IS [(`aprsis_simulate_send` = `true`)](/docs/configuration_subsections/config_testing.md). Please see the program's inline documentation for further details. 
