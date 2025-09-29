# Client Configuration

> [!TIP]
> This section configures basic content related to your personal `core-aprs-client` installation, such as your very own call sign and your TOCALL identifier.

> [!CAUTION]
> This configuration file section requires individual configuration. You HAVE to make these changes in order to install `core-aprs-client` properly.
> Keep in mind that the call signs from both `aprsis_server_filter` (see [Network Configuration](config_network.md)) AND `aprsis_callsign` need to match. If you change `aprsis_callsign` to e.g. `ABCD`, then the setting for `aprsis_server_filter` has be set to `g/ABCD` - otherwise, the [APRS-IS](https://aprs-is.net/) filter will still listen for its 'old' call sign.


You _*need*_ to modify the following values:

| Config variable   | Type  | Default value | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|-------------------|-------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprsis_callsign` | `str` | `COAC`        | Represents the call sign that the bot listens to. Change the default value `COAC` to a call sign that is not in use.                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `aprsis_tocall`   | `str` | `APRS`        | the bot's technical identifier. Once it is time to deploy your code for __production__ usage, head over to Hessu's [APRS TOCALL repository](https://github.com/aprsorg/aprs-deviceid) and request a new TOCALL for your service, then change this setting accordingy. This setting's default value `APRS` is not to be used for production purposes (but can be used during its development phase). See the [APRS Device ID](https://github.com/aprsorg/aprs-deviceid/blob/main/ALLOCATING.md#development-phase) information section for further details. |

The following settings are optional:

| Config variable                           | Type      | Default value                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                               |
|-------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprs_client_name`                        | `str`     | `Core APRS Client`                                                                                                            | Used whenever the (optional) [Apprise messaging](https://www.github.com/caronc/apprise) handler has to inform you of a program crash. See [the 'Crash Handler'](config_crash_handler.md) section for details. You should change this value to your own installation's program name - but there is no harm in keeping the default setting. |
| `aprs_input_parser_default_error_message` | `str`     | `Did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client` | This is the bot's default error message. It will be sent to the user whenever the input parser was unable to understand the user's message.                                                                                                                                                                                               |
| `aprs_message_enumeration`                | `boolean` | `False`                                                                                                                       | When set to `True`, outgoing messages will get enumerated (in case there is more than one message present). This change will allow the recipient to identify the correct order of multi-APRS messages. Note that by activating this option, the effective message content per APRS message gets reduced from 67 to 59 bytes.              |

The respective section from `core-aprs-client`'s config file lists as follows:

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
#
# This is the bot's default error message. It will be sent to the user
# whenever the input parser was unable to understand the user's message.
aprs_input_parser_default_error_message = Did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client
#
# This is the bot's default error message. It will be sent to the user
# whenever the input parser was unable to understand the user's message.
aprs_input_parser_default_error_message = Did not understand your request. Have a look at my documentation at https://github.com/joergschultzelutter/core-aprs-client
#
# Enable or disable message enumeration.
# message enumeration = True:  add trailing two-digit message number to the
#                              end of each message. Content for the max msg
#                              len gets reduced to 59 characters (excluding
#                              message number)
# message enumeration = False: do not add trailing message number to the end
#                              of each message. Message len stays at 67 chars
#
# Default setting: message enumeration = False
#
aprs_message_enumeration = False
```

> [!CAUTION]
> In case message enumeration is activated AND the user has generated more than 99 outgoing messages,
> any _additional_ messages (exceeding those 99 messages) will be purged from the outgoing queue.

Sample outputs:

`aprs_message_enumeration` = `False`:

- Output for list element 1 = `123456789012345678901234567890123456789012345678901234567890`
- Output for list element 2 = `12345678901234567890123456789012345678901234567890`

`aprs_message_enumeration` = `True` (underscore characters represent spaces):
- Output for list element 1 = `1234567890123456789012345678901234567890123456789012345_____(01/02)`
- Output for list element 1 = `12345678901234567890123456789012345678901234567890__________(02/02)`
