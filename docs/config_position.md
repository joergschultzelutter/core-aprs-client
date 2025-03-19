# Position Data

```
[position_data]
#
# Broadcast position true/false
# When set to 'true', the client will beacon its existence plus lat/lon settings
# every 4 hrs
# When set to 'false', all other parameters in this section are going to be ignored
#
aprsis_broadcast_position = false
#
# Symbol for position broadcasting
# (only used for cases where aprsis_broadcast_position = true)
# see http://www.aprs.org/symbols/symbolsX.txt
# table: APRS symbol table (/=primary \=secondary, or overlay)
# symbol: APRS symbol: Server
aprsis_table = /
aprsis_symbol = ?
#
# Latitude and longitude
# (only used for cases where aprsis_broadcast_position = true)
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
# (only used for cases where aprsis_broadcast_position = true)
aprsis_beacon_altitude_ft = 824
```

