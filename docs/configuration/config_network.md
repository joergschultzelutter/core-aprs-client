# Network Config

> [!TIP]
> This section configures basic content related to your personal ```core-aprs-client``` installation, such as your APRS-IS passcode and the APRSIS message filter. Other defaults might not require individual configuration.

> [!CAUTION]
> This configuration file section requires individual configuration. For a minimum configuration, at least the settings for ```aprsis_passcode``` and ```aprsis_server_filter``` need to be configured. 

- ```aprsis_server_name``` - the name of the APRS-IS server. Select a server from [the APRS2 Tier Network](https://www.aprs2.net/) that is close to your location.
- ```aprsis_server_port``` - our server port. Details: [see APRS-IS documentation](https://www.aprs-is.net/connecting.aspx). Normally, you don't want to change this setting.
- ```aprsis_passcode``` - the APRS-IS passcode that is valid for the configuration file's ```aprsis_callsign``` setting. If you don't know what this is, you might want to refrain from installing this program.
- ```aprsis_server_filter``` - APRS-IS's [server filter settings](https://www.aprs-is.net/javAPRSFilter.aspx). Default setting installs a call sign filter (```g/```) for our default call sign ```COAC```, thus only activating ```core-aprs-client``` whenever something is directly sent to its associated call sign.

```
#
# APRS-IS server, see https://www.aprs2.net/
aprsis_server_name = euro.aprs2.net
#
# APRS-IS port number, see https://www.aprs-is.net/connecting.aspx
# Usually, you don't want to change this
aprsis_server_port = 14580
#
# APRS-IS passcode (numeric). Replace with your very own passcode
# If you don't know what this is, then this program is not for you
aprsis_passcode = 29166
#
# APRS-IS message filter settings - see https://www.aprs-is.net/javAPRSFilter.aspx
# Ensure that both aprsis_callsign and aprsis_server_filter relate to the same call sign!
aprsis_server_filter = g/COAC
```

