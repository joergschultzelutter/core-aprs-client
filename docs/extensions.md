# Extend ```core-aprs-client``` and add your own processing code

![Workflow Input-Output Processing](../img/Workflow\ Input-Output\ Processing.drawio.svg)

By default, ```core-aprs-client```'s default installation comes with three keywords that you can send to its associated APRS call sign:

- ```greetings``` - Generate output string ```Greetings <callsign>```, meaning that your output message will be ```Greetings DF1JSL-1``` if DF1JSL-1 has sent the command to ```core-aprs-client```
- ```hello``` - Generates a "Hello World" output string
- ```error``` - Triggers the input processor`s error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of "Triggered input processor error". Your own input processor could could use this mechanism in case e.g. a keyword expects a 2nd parameter which was not supplied to ```core-aprs-client``` by the user.

Any other command that is sent to ```core-aprs-client``` will generate the bot's generic error message.

## Extending the input processor

### Input processor: Inputs
- ```from_callsign``` - the call sign that has sent the incoming APRS message to us (type: ```str```)
- ```aprs_message``` - the actual APRS message,  up to 67 bytes in length (type: ```str```)

### Input processor: Outputs
- ```success``` - ```True```in case of no errors, otherwise ```False```(type: ```boolean```)
- ```response_parameters``` - dictionary object, containing core information that is used later on for generating your output message. Details: see below

The default ```response_parameters``` object comes with three fields:
- ```from_callsign``` - same value as the input section`s ```from_callsign```
- ```input_parser_error_message``` - usually empty. If ```success == False``` AND this field is populated, ```core-aprs-client``` will output this field`s value and will not generate a default error message. You can use this field for generating custom error messages, e.g. for cases where your keyword expects a 2nd parameter which was not supplied by the user.
- ```what``` - contains an internal code which tells the program's poutput processor what it needs to do.

## Extending the output generator

### Output generator: Inputs
- ```response_parameters``` - dictionary object, containing core information from the input processor. Data structure: see previous chapter.

### Output generator: Outputs
- ```success``` - ```True```in case of no errors, otherwise ```False```(type: ```boolean```)
- ```output_message``` - ```List``` object, containing 0..n ```str``` objects of 1..67 bytes in length. 
