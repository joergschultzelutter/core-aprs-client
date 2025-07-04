# Beacon Configuration

> [!TIP]
> This section of the configuration file allows you to enable APRS beaconing (default: no beaconing). If you enable beaconing, configure parameters such as latitude/longitude, altitude, ... to your needs.

APRS Beaconing enables your `core-aprs-client` instance to appear on [aprs.fi](http://www.aprs.fi). By default, beaconing is disabled `aprsis_broadcast_beacon` = `false`, meaning that even though your bot is accessible via its call sign (`aprsis_call_sign`) in the configuration file's [client section](config_client.md), it will not announce its location data and existence to [aprs.fi](http://www.aprs.fi). `aprsis_broadcast_beacon = true` enables beaconing - and it will announce its position data, altitude, and designation to APRS-IS.


| Config variable                  | Type      | Default value     | Description                                                                                                                                                                                                                                                                                                                                                    |
|----------------------------------|-----------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aprsis_broadcast_beacon`        | `boolean` | `false`           | Global switch for disabling / enabling APRS beaconing. If set to `false`, all other following parameters are not taken into consideration.                                                                                                                                                                                                                     |
| `aprsis_table`                   | `str`     | `\`               | The COMBINATION of both `aprsis_table` and `aprsis_symbol` defines the icon type that is going to be displayed on [aprs.fi](http://www.aprs.fi). Details: see [official documentation on aprs.org](http://www.aprs.org/symbols/symbolsX.txt). You can also find graphical displays of all the available APRS icons on the Internet (search for "APRS Symbols") |
| `aprsis_symbol`                  | `str`     | `?`               | The COMBINATION of both `aprsis_table` and `aprsis_symbol` defines the icon type that is going to be displayed on [aprs.fi](http://www.aprs.fi). Details: see [official documentation on aprs.org](http://www.aprs.org/symbols/symbolsX.txt). You can also find graphical displays of all the available APRS icons on the Internet (search for "APRS Symbols") |
| `aprsis_latitude`                | `str`     | `5151.84N`        | Changes your bot's latitude location parameter. Details: [aprs101.pdf](https://www.aprs.org/doc/APRS101.PDF) chapter 6 page 23                                                                                                                                                                                                                                 |
| `aprsis_longitude`               | `str`     | `00935.48E`       | Changes your bot's longitude location parameter. Details: [aprs101.pdf](https://www.aprs.org/doc/APRS101.PDF) chapter 6 page 23                                                                                                                                                                                                                                 |
| `aprsis_beacon_altitude_ft`      | `int`     | `824`             | Changes your bot's altitude setting. Details: [aprs101.pdf](https://www.aprs.org/doc/APRS101.PDF) chapter 8. Note that the value needs to be specified in `feet` and not in `meters`.                                                                                                                                                                          |
| `aprsis_beacon_interval_minutes` | `int`     | `30` (30 minutes) | Defines your bot's beaconing interval in minutes. Default is ```30``` (minutes). Changing this setting to a smaller value is not recommended.                                                                                                                                                                                                                  |

The respective section from `core-aprs-client`'s config file lists as follows:

```
[beacon]
#
# Broadcast position beacon true/false
# When set to 'true', the client will beacon its existence plus lat/lon settings
# every 4 hrs
# When set to 'false', all other parameters in this section are going to be ignored
#
aprsis_broadcast_beacon = false
#
# Symbol for position broadcasting
# (only used for cases where aprsis_broadcast_beacon = true)
# see http://www.aprs.org/symbols/symbolsX.txt
# table: APRS symbol table (/=primary \=secondary, or overlay)
# symbol: APRS symbol: Server
aprsis_table = /
aprsis_symbol = ?
#
# Latitude and longitude
# (only used for cases where aprsis_broadcast_beacon = true)
# Location of our process (Details: see aprs101.pdf see aprs101.pdf chapter 6 pg. 23)
# Ensure to honor the format settings as described in the specification, otherwise
# your package might get rejected and/or not surface on aprs.fi
# Degrees: lat: 0-90, lon: 0-180
# Minutes and Seconds: 00-60
# Bearing: latitude N or S, longitude: E or W
# latitude=8 chars fixed length, ddmm.ssN
# longitude = 9 chars fixed length, dddmm.ssE
aprsis_latitude = 5151.84N
aprsis_longitude = 00935.48E
#
# Altitude in *FEET* (not meters) for APRS beacon. Details: see aprs101.pdf chapter 8
# (only used for cases where aprsis_broadcast_beacon = true)
aprsis_beacon_altitude_ft = 824
#
#
# Broadcast interval for beacons (default: 30 minutes)
aprsis_beacon_interval_minutes = 30
```

