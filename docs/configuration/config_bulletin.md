# Bulletin Data

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
bln0 = Core APRS Client
bln1 = See https://github.com/joergschultzelutter for
bln2 = program source code. 73 de DF1JSL
bln3 =
bln4 =
bln5 =
bln6 =
bln7 =
bln8 =
bln9 =
```
