# Crash Handler

```config
[crash_handler]
#
# Apprise config file name
# Reference to an Apprise (https://github.com/caronc/apprise) configuration file
# If value is set to NOT_CONFIGURED, Apprise messaging will be ignored
apprise_config_file = apprise.yml
#
# file name of the "nohup" file
# When you start the client, you will run something like
#
# nohup python core_aprs_client.py >nohup.out &
#
# If the apprise config is enabled AND you have specified a correct file name
# for this setting, the client will try to message you a potential call stack file
# in case the program crashes
nohup_filename="nohup.out"
```
