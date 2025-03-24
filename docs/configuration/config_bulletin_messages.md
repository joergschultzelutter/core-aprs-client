# Bulletin Configuration & Data

> [!TIP]
> This section of the configuration file allows you to configure the bulletins that you want to send out to the user; see the [bulletin configuration documentation](config_bulletin) for further info. Its conten is only used if ```aprsis_broadcast_bulletins``` is set to ```true```.

By default, ```core-aprs-client``` comes with a predefined set of 10 bulletin messages (```bln0``` to ```bln9```). You can add additional customized bulletin messages to that section as long as they follow these ground rules:

> [!NOTE]
> - The variable name used in this section will be used for broadcasting, meaning that if you create a variable ```blnhello```, the ```core-aprs-client``` will broadcast a bulletin ```BLNHELLO``` along with its associated message to the APRS users.
> - The variable name always gets converted to uppercase characters; there is no need for you to use uppercase values in the configuration file.
> - All bulletin messages' variable names MUST start with the ```BLN``` prefix. 
> - Following that fixed prefix, a combination of 6 more digits or ASCII-7 characters are permissable (0..9, a..z)
> - Duplicate key entries (e.g. ```bln0``` occurs more than once) will cause a program error.
> - Message content longer than 67 characters will be ignored.
> - Bullets use ASCII-7 character set only
> - Entries with no message content will be ignored and not broadcasted to APRS-IS

```
[bulletin_messages]
#
# APRS Bulletin messages BLN0..BLN9
# If you don't want to configure a bulletin message, then leave the value empty or
# remove the line in question
#
# Notes:
# - The variable name used in this section will be used for broadcasting, meaning that if you create a variable ```blnhello```, the ```core-aprs-client``` will broadcast a bulletin ```BLNHELLO``` along with its associated message to the APRS users.
# - The variable name always gets converted to uppercase characters; there is no need for you to use uppercase values in the configuration file.
# - All bulletin messages' variable names MUST start with the ```BLN``` prefix. 
# - Following that fixed prefix, a combination of 6 more digits or ASCII-7 characters are permissable (0..9, A..Z)
# - Duplicate key entries (e.g. ```bln0``` occurs more than once) will cause a program error.
# - Message content longer than 67 characters will get truncated
# - Bullets use ASCII-7 character set only
# - Entries with no message content will be ignored and not broadcasted to APRS-IS
#
bln0 = Core APRS Client
bln1 = See https://github.com/joergschultzelutter for
bln2 = program source code. 73 de DF1JSL
bln4 =
bln5 =
bln6 =
bln7 =
bln8 =
bln9 =
```
