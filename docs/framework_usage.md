# `core-aprs-client` framework usage

## Basic schematics
![Workflow Input-Output Processing](../img/workflow_input_output_processing.svg)

## Your custom code vs. the `core-aprs-client` framework

![Overview](../img/file_structure.drawio.svg)


## General Info

> [!INFO]
> The following documentation references the files located in this repository's [`sample_aprs_client`](/sample_aprs_client) directory

> [!TIP]
> - `input_parser.py` digests the incoming input from APRS. As an input processor, it tries to figure out what the user wants from us. If successful, the desired action is identified and returned back to the `core-aprs-client` framework - which will then forward it to the `output_generator.py` function.
> - `output_generator.py` takes the data from `input_parser.py` and builds the outgoing message which is later to be sent to APRS-IS. Note that this function is only responsible for generating the outgoing _content_ whereas `core-aprs-client` will take that data and split it up into 1..n APRS messages.

`input_parser.py` and `output_generator.py` rely on exchanging data through a mutually equal data structure. That data structure can be defined by the user and is passed through between both user functions; the `core-aprs-client` framework itself does *not* use contents from this data element (`input_parser_response_object`) _in any way_. Just ensure that both custom code modules `input_parser.py` and `output_generator.py` share the same data exchange structure. 

## Usage of the offline test option for your bot integration
> [!TIP]
> - You can use the framework's[`dryrun_testcall`](coreaprsclient_class.md#dryrun_testcall-method) method for a 100% offline testing option which does not connect to APRS-IS. `dryrun_testcall` will route a user's call sign and APRS message through both input parser and output generator modules.

## Implemented APRS Command Stubs
By default, `core-aprs-client`'s default installation comes with three keywords that you can send to its associated APRS call sign. In its default demonstration setup, the framework accepts these keywords:

| APRS Command Code | Purpose                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `greetings`       | Generate output string `Greetings <callsign>`. For example, if DF1JSL-1 has sent that command to `core-aprs-client`, its output message will be `Greetings DF1JSL-1`.                                                                                                                                                                                     |
| `hello`           | Generates a "Hello World" output string                                                                                                                                                                                                                                                                                                                   |
| `lorem`           | Generates a really long "lorem ipsum" output string which will result in multiple APRS messages. Apart from using a different text, the example is identical to the `hello` keyword.                                                                                                                                                                      |
| `error`           | Triggers the input processor's error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of `Triggered input processor error`. Your own input processor could use this mechanism in case e.g. a keyword expects an additional parameter which was not supplied to `core-aprs-client` by the user. |

Any _other_ command that is sent to `core-aprs-client` will generate the bot's _generic_ error message which is defined in the [configuration file](configuration_subsections/config_client.md).

> [!TIP]
> For demonstration purposes, both `input_parser.py` and `output_generator.py` use a _VERY_ simplified processing algorithm. For your future code, you might want to implement proper parsing (e.g. by using regular expressions) and error handling.

## Extending the input parser `input_parser.py`

### Input processor: Inputs

| Field name      | Content                                                                 | Field Type |
|-----------------|-------------------------------------------------------------------------|------------|
| `aprs_message`  | The actual APRS message that we have received, up to 67 bytes in length | `str`      |
| `from_callsign` | The call sign that has sent the incoming APRS message to us             | `str`      |

### Input processor: Outputs

| Field name                      | Content                                                                                                                                                                                                                                                                                                | Field Type                       |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `return_code`                   | Predefined `enum` object; see valid values in the [next chapter](framework_usage.md#return_code---valid-values)                                                                                                                                                                                        | `enum`                           |
| `input_parser_error_message`    | If `return_code` is not `PARSE_OK`, this field can contain an optional error message (e.g. context-specific errors related to the keyword that was sent to the bot). If this field is empty AND `return_code` is NOT `PARSE_OK`, then the default error message will be returned.                      | `str`                            |
| `input_parser_response_object`  | Dictionary object where we store the data that is required by the `output_generator` module for generating the APRS message. Note that you can also return other objects such as classes. Just ensure that both `input_parser` and `output_generator` share the very same structure for this variable. | `dict` (default) or any `object` |

#### `return_code` - Valid values

The return codes are defined in the [CoreAprsClientInputParserStatus](coreaprsclient_class.md#input_processor-return-codes) class. Import via
```
from CoreAprsClient import CoreAprsClientInputParserStatus
```
Return code details:

    # We support three possible return codes from the input parser:
    # PARSE_OK     - Input processor has identified keyword and is ready
    #                to continue. This is the desired default state
    #                Whenever the return code is PARSE_OK, then we should know
    #                by now what the user wants from us. Now, we'll leave it to
    #                another module to generate the output data of what we want
    #                to send to the user (client_output_generatpr.py).
    #                The result to this post-processor will be a general success
    #                status code and the message that is to be sent to the user.
    # PARSE_ERROR  - an error has occurred. Most likely, the external
    #                input processor was either unable to identify a
    #                keyword from the message OR a follow-up process has
    #                failed; e.g. the user has defined a wx keyword,
    #                requiring the sender to supply mandatory location info
    #                which was missing from the message. In any way, this signals
    #                the callback function that we are unable to process the
    #                message any further
    # PARSE_IGNORE - The message was ok but we are being told to ignore it. This
    #                might be the case if the user's input processor has a dupe
    #                check that is additional to the one provided by the
    #                core-aprs-client framework. Similar to PARSE_ERROR, we
    #                are not permitted to process this request any further BUT
    #                instead of sending an error message, we will simply ignore
    #                the request. Note that the core-aprs-client framework has
    #                already ack'ed the request at this point, thus preventing it
    #                from getting resend by APRS-IS over and over again.
    #
    # Note that you should refrain from using PARSE_IGNORE whenever possible - a
    # polite inquiry should always trigger a polite response :-) Nevertheless, there
    # might be use cases where you simply need to ignore a (technically valid) request
    # in your custom code.

The default `input_parser_response_object` object (as provided with the sample code) comes with two fields:

| Field name                   | Content                                                                                                                                                                                                                                                                                                                         | Field Type |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `from_callsign`              | Same value as the input section's `from_callsign`                                                                                                                                                                                                                                                                               | `str`      |
| `command_code`               | contains an internal code which tells the program's output processor what it needs to do.                                                                                                                                                                                                                                       | `str`      |

## Extending the output generator `output_generator.py`

### Output generator: Inputs

| Field name                     | Content                                                                                                                                                                                                                                                                                                | Field Type                       |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `input_parser_response_object` | Dictionary object where we store the data that is required by the `output_generator` module for generating the APRS message. Note that you can also return other objects such as classes. Just ensure that both `input_parser` and `output_generator` share the very same structure for this variable. | `dict` (default) or any `object` |
 
### Output generator: Outputs

| Field name         | Content                                                                                                                                                                                                                                                                                                                                                               | Field Type |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `success`          | `True` in case of no errors, otherwise `False`. Note that a `False` response code automatically triggers `core-aprs-client`'s default error message. If your custom `output_processor` code has failed and you still want to return a specific message to the user, you have to set this field's value to `True` and convey your data via the `output_message` field. | `boolean`  |
| `output_message`   | This is the content that will be sent to the APRS user. `core-aprs-client`'s callback function will take this content, convert it into data chunks of up to 6 bytes in length, and then send it to APRS-IS.                                                                                                                                                           | `str`      |
