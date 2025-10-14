# Network Configuration

> [!TIP]
> This section configures basic content related to your personal `core-aprs-client` installation, such as your [APRS-IS](https://aprs-is.net/) passcode and the [APRS-IS](https://aprs-is.net/) message [filter](https://aprs-is.net/javAPRSFilter.aspx). Other defaults might not require individual configuration.

> [!CAUTION]
> This configuration file section requires individual configuration.
> For a minimum valid configuration, at least the settings for `aprsis_passcode` and `aprsis_server_filter` need to get configured. 
> Keep in mind that the call signs from both `aprsis_server_filter` AND `aprsis_callsign` (see [Client Configuration](config_client.md)) __NEED__ to match. If you change `aprsis_callsign` to e.g. `ABCD`, then the setting for `aprsis_server_filter` has be set to `g/ABCD` - otherwise, the [APRS-IS](https://aprs-is.net/) filter will still listen for its 'old' call sign.

| Config variable        | Type  | Default value    | Description                                                                                                                                                                                                                                                                                           |
|------------------------|-------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprsis_server_name`   | `str` | `euro.aprs2.net` | The name of the [APRS-IS](https://aprs-is.net/) server. Select a server from [the APRS2 Tier Network](https://www.aprs2.net/) that is close to your location.                                                                                                                                         |
| `aprsis_server_port`   | `int` | `14580`          | Our [APRS-IS](https://aprs-is.net/) server port. Details: [see APRS-IS documentation](https://www.aprs-is.net/connecting.aspx). Normally, you don't want to change this setting.                                                                                                                      |
| `aprsis_passcode`      | `int` | `12345`          | The [APRS-IS](https://aprs-is.net/) passcode that is valid for the configuration file's `aprsis_callsign` [setting](config_client.md). If you don't know what this passcode is or how to calculate it, then you might want to refrain from installing this program.                                   |
| `aprsis_server_filter` | `str` | `g/COAC`         | [APRS-IS](https://aprs-is.net/)'s [server filter settings](https://www.aprs-is.net/javAPRSFilter.aspx). Default setting installs a call sign filter (`g/`) for our default call sign `COAC`, thus only activating `core-aprs-client` whenever something is directly sent to its associated call sign. |

The respective section from `core-aprs-client`'s config file lists as follows:

```
[coac_network_config]
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
aprsis_passcode = 12345
#
# APRS-IS message filter settings - see https://www.aprs-is.net/javAPRSFilter.aspx
# Ensure that both aprsis_callsign and aprsis_server_filter relate to the same call sign!
aprsis_server_filter = g/COAC
```

