# `CoreAprsClient` class

The `CoreAprsClient` class is responsible for the communication between the local APRS bot and [APRS-IS](https://aprs-is.net/). Additionally, it also provides a 'dry-run' function, allowing you to test your custom `input_parser`/`output_generator` code offline without any interaction with APRS-IS. 

Import the class via

```python
from CoreAprsClient import CoreAprsClient
```

## Class Constructor

```python
class CoreAprsClient:
    config_file: str
    log_level: int
    input_parser: Callable[..., Any]
    output_generator: Callable[..., Any]

    def __init__(
        self,
        config_file: str,
        input_parser: Callable[..., Any],
        output_generator: Callable[..., Any],
        log_level: int = logging.INFO,
    ):
```

### Parameter

| Field Name         | Description                                                                                                                                                                                                                                     | Field Type |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `config_file`      | `core_aprs_client`'s configuration file; see [this documentation section](configuration.md)                                                                                                                                                     | `str`      |
| `input_parser`     | Function name of the external input processor which parses incoming APRS messages and tries to figure out what the user wants us to do.                                                                                                         | `function` |
| `output_generator` | Function name of the external output generator. Based on the `input_parser`'s feedback, this code is responsible for generating the output message - which will then be transformed by the `core-aprs-client` framework into 1..n APRS messages | `function` |
| `log_level`        | Log level from Python's `logging` function. Default value: `logging.INFO`                                                                                                                                                                       | `enum`     |

### Supported class methods

Currently, this class supports two methods:
- [`activate_client`](coreaprsclient_class.md#activate_client-class-method) connects to [APRS-IS](https://aprs-is.net/) and exchanges data with the APRS network
- [`dryrun_testcall`](coreaprsclient_class.md#dryrun_testcall-class-method) can be used for offline testing. When triggered, it will run a simulated and freely configurable APRS input message through the `input_processor` code and, whereas applicable, uses the `output_generator` code in order to create the outgoing message content.

Additionally, a [set of specific return codes](coreaprsclient_class.md#input_processor-return-codes) have to be imported by the `input_parser` function. Finally, an optional `dict` attribute allows users to send additional dynamic APRS bulletins in addition to the statically configured bulletins. 
### Your responsibilities 

You are responsible for designing the functions associated with the `input_parser` and `output_generator` parameters. Check the [Framework Usage](framework_usage.md) help pages for further details. 

## `activate_client` class method

This class method is responsible for the communication between the local APRS bot and [APRS-IS](https://aprs-is.net/). It has no parameters. Full APRS bot client example:

```python
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

# Create the CoreAprsClient object. Supply the
# following parameters:
#
# - configuration file name
# - log level (from Python's 'logging' package)
# - function names for both input processor and output generator
#
client = CoreAprsClient(
    config_file="core_aprs_client.cfg",
    log_level=logging.INFO,
    input_parser=parse_input_message,
    output_generator=generate_output_message,
)

# Activate the APRS client
client.activate_client()
```
    
## `dryrun_testcall` class method

This class method can be used for offline testing. There will be no data exchange between [APRS-IS](https://aprs-is.net/) and the bot.

Note that this class method will not generate actual APRS response messages but rather generates the outgoing message and splits it up into 1..n message chunks of up to 67 bytes in length.

Dryrun code example:

```python
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

# Create the CoreAprsClient object. Supply the
# following parameters:
#
# - configuration file name
# - log level (from Python's 'logging' package)
# - function names for both input processor and output generator
#
client = CoreAprsClient(
    config_file="core_aprs_client.cfg",
    log_level=logging.INFO,
    input_parser=parse_input_message,
    output_generator=generate_output_message,
)

# Activate the dryrun call
client.dryrun_testcall(message_text="lorem", from_callsign="DF1JSL-1")
```

### Parameter

| Field Name      | Description                                                    | Field Type |
|-----------------|----------------------------------------------------------------|------------|
| `message_text`  | The APRS message that we are supposed to process.              | `str`      |
| `from_callsign` | Name of the callsign which has sent us the (simulated) message | `str`      |

### Sample output

This is the sample output for the `lorem` keyword from the `sample_aprs_client` provided with this repository:

``` python
2025-09-19 22:13:12,419 - CoreAprsClient -INFO - Activating dryrun testcall...
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - parsing message 'lorem' for callsign 'DF1JSL-1'
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - Parsed message:
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - {'command_code': 'loremipsum', 'from_callsign': 'DF1JSL-1'}
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - return code: CoreAprsClientInputParserStatus.PARSE_OK
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - Running Output Processor build ...
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - Output Processor response=True, message:
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
2025-09-19 22:13:12,420 - CoreAprsClient -INFO - Output processor status successful; building outgoing messages ...
2025-09-19 22:13:12,421 - CoreAprsClient -INFO - ['Lorem ipsum dolor sit amet, consetetur sadipscing elitr,    (01/11)',
 'sed diam nonumy eirmod tempor invidunt ut labore et dolore  (02/11)',
 'magna aliquyam erat, sed diam voluptua. At vero eos et      (03/11)',
 'accusam et justo duo dolores et ea rebum. Stet clita kasd   (04/11)',
 'gubergren, no sea takimata sanctus est Lorem ipsum dolor    (05/11)',
 'sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing (06/11)',
 'elitr, sed diam nonumy eirmod tempor invidunt ut labore et  (07/11)',
 'dolore magna aliquyam erat, sed diam voluptua. At vero eos  (08/11)',
 'et accusam et justo duo dolores et ea rebum. Stet clita     (09/11)',
 'kasd gubergren, no sea takimata sanctus est Lorem ipsum     (10/11)',
 'dolor sit amet.                                             (11/11)']
```

## `input_processor` return codes

Unlike the `output_generator` which either provides a success/failure scenario, the `input_processor` supports _**three**_ return codes. Your custom `input_processor` code needs to import those via

```python
from CoreAprsClient import CoreAprsClientInputParserStatus
```

Valid values:

```python
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
```
    
> [!IMPORTANT]
> `PARSE_IGNORE` should _only_ be used for cases where your custom input processor has implemented e.g. a dupe check that is _additional_ to `core-aprs-client`s dupe check and you don't want to trigger ANY response to the user's inquiry. In any other case, use `PARSE_ERROR` and return a proper response message to the user.

### `input_processor` return code sample

```python
from CoreAprsClient import CoreAprsClientInputParserStatus

def process_the_input():
    ....
    do some processing
    input_parser_response_object = {"key" : "value"}
    ....

    return_code = CoreAprsClientInputParserStatus.PARSE_OK if there_was_no_error else CoreAprsClientInputParserStatus.PARSE_ERROR
    input_parser_error_message = "my_custom_error_message" if there_was_no_error else ""
    return return_code, input_parser_error_message, input_parser_response_object
```

## Use of dynamic content for APRS bulletins additional to static bulletin content

> [!NOTE]
> Optional extension; in most cases, you will not need to use this function.

As [described in the framework documentation](configuration_subsections/config_bulletin.md), `core-aprs-framework` can send to the [APRS-IS](https://aprs-is.net/) framework at the user's request. The associated bulletin messages are stored as static content [in the configuration file](configuration_subsections/config_bulletin_messages.md). 

In addition to the static bulletin messages configured in the `core-aprs-client`'s configuration file, it is also possible to send dynamic bulletin messages. These could be, for example, special weather data that is only determined during the runtime of the bot. [mpad](https://www.github.com/joergschultzelutter/mpad) uses this, for example, to send out [hazard warnings from the local German weather service](https://github.com/joergschultzelutter/mpad/blob/master/docs/INSTALLATION.md#program-configuration).

> [!IMPORTANT]
> The ability to send this dynamic data is provided by a variable of type ‘dict’. :heavy_exclamation_mark:**The associated dictionary within the class must always be replaced in its _entirety_**, as thread safety has only been implemented for this method. :heavy_exclamation_mark:

The following conditions apply:

* The default value of this separate variable is an empty ‘dict’ object; i.e., no dynamic bulletins are available
* To send dynamic bulletins, the function for sending static bulletins (i.e., the contents of the configuration file) must be activated (`aprsis_broadcast_bulletins` = `true`). It is generally possible not to preassign the static contents of the bulletins and to use only dynamic contents.
* Like static bulletins, dynamic bulletins must meet the requirements of the APRS specification, which are defined [in Chapter 14 of the APRS specifications](https://github.com/wb2osz/aprsspec) (_Messages, Bulletins, and Announcements_).
  * Dynamic Bulletins begin with the prefix `BLN` or `NWS` and follow the format specifications of the APRS specifications, depending on the selected prefix. 
  * The text content uses ASCII-7 bit and is up to 67 characters long per bulletin. When transferring longer content, a `ValueError` exception is thrown. 
  * Special characters `{}|~` are automatically removed from the outgoing message by `core-aprs-client`. 
  * Garbage in, garbage out. With great power comes great responsibility.