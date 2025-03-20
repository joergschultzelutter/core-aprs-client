# Bulletin Data

> [!TIP]
> This section of the configuration file allows you to enable APRS bulletin broadcasting. APRS supports 10 bulletins (BLN0..9) which can be used for broadcasting static or dynamic texts to _all_ APRS users. Bulletin messages are received by nearby APRS-capable transceivers and [can be viewed on aprs.fi](https://aprs.fi/bulletin/).

By default, the APRS bulletin data function is disabled (```aprsis_broadcast_bulletins = false```), meaning that ```core-aprs-client``` will not broadcast any APRS bulletins for you. If you change this setting to ```true```, then ```core-aprs-client``` will broadcast all _populated_ bulletin entries (```bln0``` to ```bln9```) in the configuration file with a fixed broadcasting interval of 4 hours.

> [!NOTE]
> - Duplicate key entries (e.g. ```bln0``` occurs more than once) will be ignored.
> - Messages longer than 67 characters will get truncated
> - Ensure to stick to the ASCII-7 character set

```
[bulletin_data]
#
# Broadcast APRS bulletins (BLN0..9) true/false
# When set to 'true', the client will beacon a FIXED set of APRS bulletin messages
# every 4 hrs.
# When set to 'false', all other parameters in this section are going to be ignored
aprsis_broadcast_bulletins = false
#
# APRS Bulletin messages BLN0..BLN9
# If you don't want to configure a bulletin message, then leave the value empty or
# remove the line in question
#
# Notes:
# - Duplicate keys will be ignored
# - any key that is NOT a bulletin will be ignored
# - messages longer than 67 characters will get truncated
# - Ensure to stick with the ASCII-7 character set
#
aprsis_bln0 = Core APRS Client
aprsis_bln1 = See https://github.com/joergschultzelutter for
aprsis_bln2 = program source code. 73 de DF1JSL
aprsis_bln3 =
aprsis_bln4 =
aprsis_bln5 =
aprsis_bln6 =
aprsis_bln7 =
aprsis_bln8 =
aprsis_bln9 =
#
# Broadcast interval for bulletins (default: 240 minutes = 4 hours)
aprsis_bulletin_interval_minutes = 240
```
