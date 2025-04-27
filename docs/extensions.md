# Extending `core-aprs-client` with your own bot processing code

![Workflow Input-Output Processing](../img/workflow_input_output_processing.svg)

> [!TIP]
> - `client_input_parser.py` digests the incoming input from APRS. As an input processor, it tries to figure out what the user wants from us.
> - `client_output_generator.py` takes the data from `client_input_parser.py` and builds the outgoing message which is later to be sent to APRS-IS.
> - You can always use 'testcall.py' for a 100% offline testing option.

By default, `core-aprs-client`'s default installation comes with three keywords that you can send to its associated APRS call sign:

| APRS Command Code | Purpose                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `greetings`       | Generate output string `Greetings <callsign>`. For example, if DF1JSL-1 has sent that command to `core-aprs-client`, its output message will be `Greetings DF1JSL-1`.                                                                                                                                                                                     |
| `hello`           | Generates a "Hello World" output string                                                                                                                                                                                                                                                                                                                   |
| `error`           | Triggers the input processor's error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of `Triggered input processor error`. Your own input processor could use this mechanism in case e.g. a keyword expects an additional parameter which was not supplied to `core-aprs-client` by the user. |

Any _other_ command that is sent to `core-aprs-client` will generate the bot's _generic_ error message, such as `Unknown command`.

> [!TIP]
> For demonstration purposes, both `client_input_parser.py` and `client_output_generator.py` use a _very_ simplified processing algorithm. For your future code, you might want to implement proper parsing (e.g. by using regular expressions) and error handling.

## Extending the input parser `client_input_parser.py`

### Input processor: Inputs

| Field name      | Content                                                     | Field Type |
|-----------------|-------------------------------------------------------------|------------|
| `from_callsign` | The call sign that has sent the incoming APRS message to us | `str`      |
| `aprs_message`  | the actual APRS message,  up to 67 bytes in length          | `str`      |

### Input processor: Outputs

| Field name            | Content                                                                                  | Field Type |
|-----------------------|------------------------------------------------------------------------------------------|------------|
| `success`             | `True` in case of no errors, otherwise `False`                                           | `boolean`  |
| `response_parameters` | the actual APRS message; up to 67 bytes in length. Details: see section below this table | `dict`     |


The default `response_parameters` object comes with three fields:

| Field name                   | Content                                                                                                                                                                                                                                                                                                                         | Field Type |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `from_callsign`              | Same value as the input section's `from_callsign`                                                                                                                                                                                                                                                                               | `str`      |
| `input_parser_error_message` | usually empty. If `success == False` AND this field is populated, `core-aprs-client` will output this field's value and will not generate a _default_ error message. You can use this field for generating custom error messages, e.g. for cases where your keyword expects a 2nd parameter which was not supplied by the user. | `str`      |
| `command_code`               | contains an internal code which tells the program's output processor what it needs to do.                                                                                                                                                                                                                                       | `str`      |

## Extending the output generator `client_output_generator.py`

### Output generator: Inputs

| Field name            | Content                                                                          | Field Type |
|-----------------------|----------------------------------------------------------------------------------|------------|
| `response_parameters` | the actual APRS message; up to 67 bytes in length. Details: see previous chapter | `dict`     |

### Output generator: Outputs

| Field name         | Content                                                                                                                        | Field Type |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------|------------|
| `success`          | `True` in case of no errors, otherwise `False`                                                                                 | `boolean`  |
| `output_message`   | `List` object, containing 1..n `str` objects of 1..67 bytes in length. This is the content that will be sent to the APRS user. | `list`     |

Any errors which may arise as part of the `output-generator` process should be part of the `output_message` field. You can still check for the `success` field's value, though.
