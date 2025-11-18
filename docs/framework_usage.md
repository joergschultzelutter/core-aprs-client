# `core-aprs-client` framework usage

## Basic schematics
![Workflow Input-Output Processing](/img/workflow_input_output_processing.svg)

## Your custom code vs. the `core-aprs-client` framework

![Overview](/img/file_structure.svg)


## General Info

> [!NOTE]
> The following documentation references the files located in this repository's [`framework_examples`](/framework_examples) directory

> [!TIP]
> - [`input_parser.py`](/framework_examples/input_parser.py) digests the incoming input from APRS. As an input processor, it tries to figure out what the user wants from us. If successful, the desired action is identified and returned back to the `core-aprs-client` framework - which will then forward it to the `output_generator.py` function.
> - [`output_generator.py`](/framework_examples/output_generator.py) takes the data from [`input_parser.py`](/framework_examples/input_parser.py) and builds the outgoing message which is later to be sent to APRS-IS. Note that this function is only responsible for generating the outgoing _content_ whereas `core-aprs-client` will take that data and split it up into 1...n APRS messages. Dependent on your use case, [`output_generator.py`](/framework_examples/output_generator.py) might also generate data for those edge cases where you want to have `core-aprs-client` execute an action _after_ the APRS response has been sent to the user. That data will get digested by [`post_processor.py`](/framework_examples/post_processor.py) if the user has assigned a post processing function to the class' instance.
> - [`post_processor.py`](/framework_examples/post_processor.py) takes the data from [`output_generator.py`](/framework_examples/output_generator.py) and executes a custom function _after_ the APRS response has been sent to the user, assuming that the user has assigned such a post-processing function to the class' instance.
> - Both function names and file names do not need to follow a naming pattern and can reside e.g. in a single file; the file structure in this repository has only been chosen for illustration purposes. 

`input_parser.py` and `output_generator.py` rely on exchanging data through a mutually equal data structure. That data structure can be defined by the user and is passed through between both user functions; the `core-aprs-client` framework itself does *not* use contents from this data element (`input_parser_response_object`) _in any way_. Just ensure that both custom code modules `input_parser.py` and `output_generator.py` share the same data exchange structure. Note that the same setup also applies to the data exchange between `output_generator.py` and `post_processor.py`.

![DataExchange](/img/data_exchange.svg)

## Usage of the offline test option for your bot integration
> [!TIP]
> - You can use the framework's[`dryrun_testcall`](coreaprsclient_class.md#dryrun_testcall-class-method) method for a 100% offline testing option which does not connect to APRS-IS. `dryrun_testcall` will route a user's call sign and APRS message through both input parser and output generator modules: it also covers the post processor function logic.

## Implemented APRS Command Stubs
By default, `core-aprs-client`'s default installation comes with sample keywords that you can send to its associated APRS call sign. In its default demonstration setup, the framework accepts these keywords:

| APRS Command Code | Purpose                                                                                                                                                                                                                                                                                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `greetings`       | Generate output string `Greetings <callsign>`. For example, if DF1JSL-1 has sent that command to `core-aprs-client`, its output message will be `Greetings DF1JSL-1`.                                                                                                                                                                                     |
| `hello`           | Generates a "Hello World" output string                                                                                                                                                                                                                                                                                                                   |
| `lorem`           | Generates a really long "lorem ipsum" output string which will result in multiple APRS messages. Apart from using a different text, the example is identical to the `hello` keyword.                                                                                                                                                                      |
| `postproc`        | Similar to the `hello` keyword. Illustrates the usage of `core-aprs-client`'s post processor options (trigger an action _after_ the APRS response message has been sent to the user. Note that for using the postprocessor option, you also need to provide a custom postprocessor function to the framework - see the `framework_examples` folder.       |
| `error`           | Triggers the input processor's error mechanism and generates an input-processor specific error. This demo will use a fixed string with the value of `Triggered input processor error`. Your own input processor could use this mechanism in case e.g. a keyword expects an additional parameter which was not supplied to `core-aprs-client` by the user. |

Any _other_ command that is sent to `core-aprs-client` will generate the bot's _generic_ error message which is defined in the [configuration file](configuration_subsections/config_client.md).

> [!TIP]
> For demonstration purposes, both `input_parser.py` and `output_generator.py` use a _VERY_ simplified processing algorithm. For your future code, you might want to implement proper parsing (e.g. by using regular expressions) and error handling.

> [!NOTE]
> - All input parameters for `input_parser.py`, `output_generator.py`, and `post_processor.py` are mandatory parameters
> - Internally, all input parameters are treated as named parameters.

## Extending the input parser [`input_parser.py`](/framework_examples/input_parser.py)

```python
def parse_input_message(instance: CoreAprsClient,
                        aprs_message: str, 
                        from_callsign: str, 
                        **kwargs):
    ....
    return  (return_code, 
             input_parser_error_message, 
             input_parser_response_object)
```


### Input processor: Inputs

| Field name      | Content                                                            | Field Type       |
|-----------------|--------------------------------------------------------------------|------------------|
| `instance`      | Your `core-aprs-client` instance                                   | `CoreAprsClient` |
| `aprs_message`  | The actual APRS message that we have received from `from_callsign` | `str`            |
| `from_callsign` | The call sign that has sent the incoming APRS message to us        | `str`            |
| `**kwargs`      | Optional user-defined parameters                                   | `dict`           |

### Input processor: Outputs

| Field name                      | Content                                                                                                                                                                                                                                                                                                | Field Type                       |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `return_code`                   | Predefined `enum` object; see valid values in the [next chapter](framework_usage.md#return_code---valid-values)                                                                                                                                                                                        | `enum`                           |
| `input_parser_error_message`    | If `return_code` is not `PARSE_OK`, this field can contain an optional error message (e.g. context-specific errors related to the keyword that was sent to the bot). If this field is empty AND `return_code` is NOT `PARSE_OK`, then the default error message will be returned.                      | `str`                            |
| `input_parser_response_object`  | Dictionary object where we store the data that is required by the `output_generator` module for generating the APRS message. Note that you can also return other objects such as classes. Just ensure that both `input_parser` and `output_generator` share the very same structure for this variable. | `dict` (default) or any `object` |

#### `return_code` - Valid values

The return codes are defined in the [CoreAprsClientInputParserStatus](coreaprsclient_class.md#input_processor-return-codes) class. Import via
```python
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

## Extending the output generator [`output_generator.py`](/framework_examples/output_generator.py)

```python
def generate_output_message(
    instance: CoreAprsClient,
    input_parser_response_object: dict | object, 
    default_error_message: str,
    **kwargs
):
    ...
    return  (success, 
             output_message, 
             postprocessor_input_object)
```

The output generator has only one input parameter: the input parser's response object.


### Output generator: Inputs

| Field name                     | Content                                                                                                                                                                                                                                                                                                  | Field Type                       |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `instance`                     | Your `core-aprs-client` instance                                                                                                                                                                                                                                                                         | `CoreAprsClient`                 |
| `input_parser_response_object` | (Dictionary) object where we store the data that is required by the `output_generator` module for generating the APRS message. Note that you can also return other objects such as classes. Just ensure that both `input_parser` and `output_generator` share the very same structure for this variable. | `dict` (default) or any `object` |
| `**kwargs`                     | Optional user-defined parameters                                                                                                                                                                                                                                                                         | `dict`                           |
 
### Output generator: Outputs

| Field name                   | Content                                                                                                                                                                                                                                                                                                                                                                                                       | Field Type         |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| `success`                    | `True` in case of no errors, otherwise `False`. Note that a `False` response code automatically triggers `core-aprs-client`'s default error message. If your custom `output_processor` code has failed and you still want to return a specific message to the user, you have to set this field's value to `True` and convey your data via the `output_message` field.                                         | `boolean`          |
| `output_message`             | This is the content that will be sent to the APRS user. `core-aprs-client`'s callback function will take this content, convert it into data chunks of up to 6 bytes in length, and then send it to APRS-IS.                                                                                                                                                                                                   | `str`              |
| `postprocessor_input_object` | Optional. If you want to use the framecwork's post-processing options (perform an action _after_ the APRS response has been sent to the user, populate this field and add a custom function to `core-aprs-client`'s class instance. Simlar to `input_parser_response_object`, the content is just passed along to the post processor, meaning that you can use e.g. `dict` objects or custom data structures. | `object` or `None` |

## Extending the post processor [`post_processor.py`](/framework_examples/post_processor.py)

> [!NOTE]
> Usage of the post processor function is optional. You only want to use if for those cases where an additional action is supposed to be triggered _after_ the APRS response has been sent back to the user.

```python
def post_processing(
    instance: CoreAprsClient,
    postprocessor_input_object: dict | object, 
    **kwargs
):
    ...
    return success
```

The post processor has only one input parameter: a simple `True`/`False` response whose value currently is of no consequence for the `core-aprs-client` framework.


### Post Processor: Inputs

| Field name                   | Content                                                                                                                                                                                                                                                                                                                                 | Field Type                       |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `instance`                   | Your `core-aprs-client` instance                                                                                                                                                                                                                                                                                                        | `CoreAprsClient`                 |
| `postprocessor_input_object` | (Dictionary) object where we store the data that is required by the `post_processor` module for the individual post processing action. The data type can be anything from a simple string, dictionary to a class object. Just ensure that both `output_generator` and `post_processor` share the very same structure for this variable. | `dict` (default) or any `object` |
| `**kwargs`                   | Optional user-defined parameters                                                                                                                                                                                                                                                                                                        | `dict`                           |
 
### Post Processor: Outputs

| Field name | Content                                                                                                                                   | Field Type |
|------------|-------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `success`  | `True` in case of no errors, otherwise `False`. Note that with the current version of `core-aprs-client`, the value is of no consequence. | `boolean`  |
