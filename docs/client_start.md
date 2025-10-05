## Running the sample APRS client

The sample APRS client can be accessed [here](https://github.com/joergschultzelutter/core-aprs-client/tree/master/sample_aprs_client).

Every configuration setting is stored in the program's config file - see the documentation on [the program's configuration file](configuration.md). Therefore, the only command line option that can be specified is the name of the configuration file.

```python
usage: sample_aprs_client.py [-h] [--configfile CONFIGFILE]

options:
  -h, --help                show this help message and exit
  --configfile CONFIGFILE   Program config file name (default is 'core_aprs_client.cfg')
```
 Ideally, run the program via `nohup python sample_aprs_client.py >nohup.out &`. See also [the config file's section on the crash handler](configuration_subsections/config_crash_handler.md) on how to use the `nohup.out` file in case of program crashes.
