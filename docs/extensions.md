# Extend core-aprs-client and add your own processing code

![Workflow Input-Output Processing](../img/Workflow\ Input-Output\ Processing.drawio.svg)

By default, ```core-aprs-client```'s default installation comes with three keywords that you can send to its associated APRS call sign:

- ```greetings``` - Generate output string ```Greetings <callsign>```, meaning that your output message will be ```Greetings DF1JSL-1``` if DF1JSL-1 has sent the command to ```core-aprs-client```
- ```hello``` - Generates a "Hello World" output string
- ```error``` - Triggers the input processor`s error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of "Triggered input processor error". Your own input processor could could use this mechanism in case e.g. a keyword expects a 2nd parameter which was not supplied to ```core-aprs-client``` by the user.

Any other command that is sent to ```core-aprs-client``` will generate the bot's generic error message.


