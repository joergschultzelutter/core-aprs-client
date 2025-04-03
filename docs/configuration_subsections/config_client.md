# Client Config

> [!TIP]
> This section configures basic content related to your personal ```core-aprs-client``` installation, such as your very own call sign and your TOCALL identifier.

> [!CAUTION]
> This configuration file section requires individual configuration. You HAVE to make these changes in order to install ```core-aprs-client``` properly.

You _*need*_ to modify the following values:

- ```aprsis_callsign``` is the call sign that the bot listens to. Change the default value ```COAC``` to a call sign that is not in use.
- ```aprsis_tocall``` is equivalent to the bot's technical identifier. Head over to Hessu's [APRS TOCALL repository](https://github.com/aprsorg/aprs-deviceid) and request a new TOCALL for your service, then change this setting accordingy. This setting's default value ```APRS``` in not to be used on a permanent basis.
- ```aprs_client_name``` is used whenever the (optional) Apprise handler has to inform you of a program crash. See [the 'Crash Handler'](config_crash_handler.md) section for details. You should change this value to your own installation's program name - but there is no harm in keeping the default setting. 

```
[client_config]
#
# APRS Listener call sign. Default call sign is COAC
# This is the call sign on which the APRS client listens to
# while being connected to APRS-IS. Read: you have to send
# your messages to this call sign
# Change BOTH aprsis_callsign and aprsis_server_filter settings
# in case you want to use a different call sign
aprsis_callsign = COAC
#
# This is the APRS "tocall" identifier which is used for outgoing messages
# You NEED to request your very own TOCALL for your own client code
# Details: https://github.com/aprsorg/aprs-deviceid
aprsis_tocall = APRS
#
# This variable is used by the Apprise communication subroutines
# Its contents are freely configurable and will be used in case
# of program crashes (e.g. Telegram messages to the bot's host)
aprs_client_name = Core APRS Client
```
