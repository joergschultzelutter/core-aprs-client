# Network Config

> [!TIP]
> This section configures basic content related to your personal ```core-aprs-client``` installation, such as your APRS-IS passcode and the APRSIS message filter. Other defaults might not require individual configuration.

> [!CAUTION]
> Requires individual configuration

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

