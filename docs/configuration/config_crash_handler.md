# Crash Handler

> [!NOTE]
> These are optional settings for the bot's crash handler. When activated, the bot will (try to) send you a crash notification prior to its program termination. For this task, the bot uses the [Apprise Notification Library](http://www.github.com/caronc/apprise) whose messenger configuration depends on an external configuration file. If both Apprise messenger configuration file AND the bot's crash file are present, then ```core-aprs-client``` will try to send you a zipped version of that file - which will make it easier for you to both detect program crashes and also determine its potential root cause (thanks to being able to access that log file).

- ```apprise_config_file``` is the [Apprise Notification Library](http://www.github.com/caronc/apprise) config file. An Apprise demo template file has been added to this repository. Omit a file name value or set it to ```NOT_CONFIGURED``` in order to deactivate the crash handler.
- ```nohup_filename``` is the name of the file that we have to send to the user in case the client has crashed. For example, assume that we started the ```core-aprs-cient``` by initiating ```nohup python core_aprs_client.py >nohup.out &```, then ```nohup.out``` would need to be specified as value. Omit a file name value or set it to ```NOT_CONFIGURED``` in order to deactivate the crash handler.

```bash
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
nohup_filename = nohup.out
```
