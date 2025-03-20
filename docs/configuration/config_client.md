# Client Config

> [!TIP]
> This section configures basic content related to your personal ```core-aprs-client``` installation, such as your very own call sign and your TOCALL identifier.

> [!CAUTION]
> Requires individual configuration

You _*need*_ to modify the following values:

- ```aprsis_callsign``` is the call sign that the bot listens to. Change the default value ```COAC``` to a call sign that is not in use.
- ```aprsis_tocall``` is equivalent to the bot's technical identifier. Head over to Hessu's [APRS TOCALL repository](https://github.com/aprsorg/aprs-deviceid) and request a new TOCALL for your service, then change this setting accordingy. This setting's default value ```APRS``` in not to be used on a permanent basis.

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
```
