# Client Config

:::! "Warning"
Mandatory configuration setting - you HAVE to change this
:::

```
[client_config]

# This is the configuration file for the Core APRS Client
#
# APRS Listener call sign
# Default call sign is COAC (*CO*re *A*prs *C*lient)
# Change BOTH aprsis_callsign and aprsis_server_filter settings
# in case you want to use a different call sign
#
# This is the call sign on which the APRS client listens to
# while being connected to APRS-IS. Read: you have to send
# your messages to this call sign
aprsis_callsign = COAC
#
# This is the APRS "tocall" identifier that is used for outgoing messages
# You NEED to request your very own TOCALL for your client code
# Details: https://github.com/aprsorg/aprs-deviceid
aprsis_tocall = APRS
```
