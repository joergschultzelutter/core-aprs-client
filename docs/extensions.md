# Extend ```core-aprs-client``` and add your own processing code

![Workflow Input-Output Processing](../img/workflow_input_output_processing.svg)

> [!TIP]
> - ```client_input_parser.py``` digests the incoming input from APRS. As an input processor, it tries to figure out what the user wants from us.
> - ```client_output_generator.py``` takes the data from ```client_input_parser.py``` and builds the outgoing message which is later to be sent to APRS-IS.

By default, ```core-aprs-client```'s default installation comes with three keywords that you can send to its associated APRS call sign:

- ```greetings``` - Generate output string ```Greetings <callsign>```, meaning that your output message will be ```Greetings DF1JSL-1``` if DF1JSL-1 has sent the command to ```core-aprs-client```
- ```hello``` - Generates a "Hello World" output string
- ```error``` - Triggers the input processor's error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of ```Triggered input processor error```. Your own input processor could use this mechanism in case e.g. a keyword expects an additional parameter which was not supplied to ```core-aprs-client``` by the user.

Any _other_ command that is sent to ```core-aprs-client``` will generate the bot's _generic_ error message, such as ```Unknown command```.

> [!TIP]
> For demonstration purposes, both ```client_input_parser.py``` and ```client_output_generator.py``` use a _very_ simplified processing algorithm. For your future code, you might want to implement proper parsing (e.g. by using regular expressions) and error handling.

## Extending the input parser ```client_input_parser.py```

### Input processor: Inputs
- ```from_callsign``` - the call sign that has sent the incoming APRS message to us (type: ```str```)
- ```aprs_message``` - the actual APRS message,  up to 67 bytes in length (type: ```str```)

### Input processor: Outputs
- ```success``` - ```True```in case of no errors, otherwise ```False```(type: ```boolean```)
- ```response_parameters``` - dictionary object, containing core information that is used later on for generating your output message. Details: see below

The default ```response_parameters``` object comes with three fields:
- ```from_callsign``` - same value as the input section`s ```from_callsign```
- ```input_parser_error_message``` - usually empty. If ```success == False``` AND this field is populated, ```core-aprs-client``` will output this field`s value and will not generate a default error message. You can use this field for generating custom error messages, e.g. for cases where your keyword expects a 2nd parameter which was not supplied by the user.
- ```command_code``` - contains an internal code which tells the program's output processor what it needs to do.

## Extending the output generator ```client_output_generator.py```

### Output generator: Inputs
- ```response_parameters``` - dictionary object, containing core information from the input processor. Data structure: see previous chapter.

### Output generator: Outputs
- ```success``` - ```True```in case of no errors, otherwise ```False```(type: ```boolean```)
- ```output_message``` - ```List``` object, containing 0..n ```str``` objects of 1..67 bytes in length. This is the content that will be sent to the APRS user.

Any errors which may arise as part of the ```output-generator``` process should be part of the ```output_message``` field. You can still check for the ```success``` field's value, though.
