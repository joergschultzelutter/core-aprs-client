# `CoreAprsClient` class

The `CoreAprsClient` class is responsible for the communication between the local APRS bot and [APRS-IS](https://aprs-is.net/). Additionally, it also provides a 'dry-run' function, allowing you to test your custom `input_parser`/`output_generator` code offline without any interaction with APRS-IS. 

> [!TIP]
> Examples of all class methods can be found in the [`framework_examples`](/framework_examples/README.md) directory



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
    post_processor: Callable[..., Any] | None

    def __init__(
        self,
        config_file: str,
        input_parser: Callable[..., Any],
        output_generator: Callable[..., Any],
        post_processor: Callable[..., Any] | None = None,
        log_level: int = logging.INFO,
    ):
```

### Parameter

| Field Name         | Description                                                                                                                                                                                                                                     | Field Type |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| `config_file`      | `core_aprs_client`'s configuration file; see [this documentation section](configuration.md)                                                                                                                                                     | `str`      |
| `input_parser`     | Function name of the external input processor which parses incoming APRS messages and tries to figure out what the user wants us to do.                                                                                                         | `Callable` |
| `output_generator` | Function name of the external output generator. Based on the `input_parser`'s feedback, this code is responsible for generating the output message - which will then be transformed by the `core-aprs-client` framework into 1..n APRS messages | `Callable` |
| `post_processor`   | Optional. Function name of an external post processing function. Triggered by `output_generator` providing post-processing data to the framework. Executed _after_ the APRS response has been sent to the user.                                 | `Callable` |
| `log_level`        | Log level from Python's `logging` function. Default value: `logging.INFO`                                                                                                                                                                       | `enum`     |

### Supported class methods

Currently, this class supports the following methods:
- [`activate_client`](coreaprsclient_class.md#activate_client-class-method) connects to [APRS-IS](https://aprs-is.net/) and exchanges data with the APRS network
- [`dryrun_testcall`](coreaprsclient_class.md#dryrun_testcall-class-method) can be used for offline testing. When triggered, it will run a simulated and freely configurable APRS input message through the `input_processor` code and, whereas applicable, uses the `output_generator` code in order to create the outgoing message content.

Additionally, a [set of specific return codes](coreaprsclient_class.md#input_processor-return-codes) have to be imported by the `input_parser` function. Finally, an optional `dict` attribute allows users to send additional dynamic APRS bulletins in addition to the statically configured bulletins. A 'getter' method allows you to retrieve the (immutable) `dict` object of the class' configuration file data, thus allowing you to store your specific configuration file content in `core-aprs-client`'s config file. 

### Your responsibilities 

You are responsible for designing the functions associated with the `input_parser` and `output_generator` parameters (plus `post_processor` in case post processing code is required). Check the [Framework Usage](framework_usage.md) help pages for further details. 

## `activate_client` class method

Sample code: [`demo_aprs_client.py`](/framework_examples/demo_aprs_client.py)

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

# Activate the APRS client without additional user data (default)
client.activate_client()

# Activate the APRS client with additional user parameters
#client.activate_client(hello="world", lorem="ipsum")
```
### Parameters

| Field name      | Content                                                            | Field Type |
|-----------------|--------------------------------------------------------------------|------------|
| `**kwargs`      | Optional user-defined parameters                                   | `dict`     |

Any `**kwargs` arguments will get passed along to both `input_parser` and `output_generator` (and `post_processor` if a custom post processor has been provided by the user).

### Return values

This method has no return values

    
## `dryrun_testcall` class method

Sample_code: [`demo_dryrun.py`](/framework_examples/demo_dryrun.py)

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

# Activate the dryrun call witout additional user data (default)
client.dryrun_testcall(message_text="lorem", from_callsign="DF1JSL-1")

# Activate the dryrun testcall with additional user data
#client.dryrun_testcall(message_text="lorem", from_callsign="DF1JSL-1", hello="world", lorem="ipsum")
```

### Parameters

| Field Name      | Description                                                    | Field Type |
|-----------------|----------------------------------------------------------------|------------|
| `message_text`  | The APRS message that we are supposed to process.              | `str`      |
| `from_callsign` | Name of the callsign which has sent us the (simulated) message | `str`      |
| `**kwargs`      | Optional user-defined parameters                               | `dict`     |

Any `**kwargs` arguments will get passed along to both `input_parser` and `output_generator`.


### Return values

This method has no return values

### Sample output

This is the sample output for the `lorem` keyword from the [`demo_dryrun.py`](/framework_examples/demo_dryrun.py) sample code provided [with this repository](/framework_examples):

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

## `send_apprise_message` class method

This is a wrapper for the [Apprise messaging](https://www.github.com/caronc/apprise) features. You can use this feature to send messages to messenger accounts. For example, [`mpad`](https://github.com/joergschultzelutter/mpad) uses this feature internally to alert you to errors during regular downloads of external files, in case one of the source URLs might have changed.

Apprise code example:

```python
# This sends a fixed test message to 1..n messenger
# clients via Apprise. By omitting the apprise_cfg_file
# value, we tell the framework to use the Apprise config
# file name from core-aprs-client's config file (see
# https://github.com/joergschultzelutter/core-aprs-client/blob/apprise-messaging-method/docs/configuration_subsections/config_crash_handler.md
# for further info. Alternatively, you can specify your very own
# Apprise configuration file name.
#
# Note that a missing Apprise config file will not result in an
# error but simply generates a log file error instead. By examining
# the given return code, you can still decide to abort your program
# afterwards, if necessary

client.send_apprise_message(
    msg_header="Hello from Apprise",
    msg_body="This is a demo message",
    msg_attachment=None,
    apprise_cfg_file=None,
)
```

### Sample output

```python
2025-10-20 20:44:06,214 - demo_apprise_message -INFO - Starting demo module: Apprise messaging
2025-10-20 20:44:06,214 - demo_apprise_message -INFO - This is a demo APRS client which sends a fixed demo message via Apprise to 1..n messaging clients
2025-10-20 20:44:06,217 - CoreAprsClient -DEBUG - No apprise_cfg_file specified; using default from core-aprs-client's configuration file
2025-10-20 20:44:06,217 - client_utils -DEBUG - Starting Apprise message processing
2025-10-20 20:44:06,467 - base -INFO - Loaded 1 entries from file://apprise.yml?encoding=utf-8&cache=yes
2025-10-20 20:44:06,693 - telegram -INFO - Sent Telegram notification.
2025-10-20 20:44:06,694 - client_utils -DEBUG - Finished Apprise message processing
```

### Parameters

| Field Name         | Description                                                                                                                                                                                                                                                                                       | Field Type      |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `msg_header`       | Apprise message header. Dependent on the selected messenger type, this field's value may get omitted.                                                                                                                                                                                             | `str`           |
| `msg_body`         | Apprise message body (aka the message that you want to send to the messenger account(s)                                                                                                                                                                                                           | `str`           |
| `msg_attachment`   | File name of an external file that is to be sent as attachment or `None` (default value) if no attachment is supposed to be used                                                                                                                                                                  | `str` or `None` |
| `apprise_cfg_file` | File name the [Apprise YAML Configuration File](https://github.com/caronc/apprise/wiki/config_yaml). If set to `None` (default value), the Apprise configuration file name is determined by the value from the framework configuration file's [`crash handler`](config_crash_handler.md) section. | `str` or `None` |


> [!NOTE]
> A missing `apprise_cfg_file` will NOT result in a program error. The missing file name will end up as notification in the program log file and you will receive a `success` value of `False`. You can still abort your code afterwards, if necessary.

### Return values

| Field Name | Description                                                     | Field Type |
|------------|-----------------------------------------------------------------|------------|
| `success`  | `True` if message was sent to Apprise module, otherwise `False` | `bool`     |

A `success` value of `True` describes the situation where the Apprise module has accepted the incoming message. It does not necessarily guarantee that the message was actually sent to the messenger recipient clients.

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

def parse_input_message(aprs_message: str, from_callsign: str, **kwargs):
    ....
    do some processing
    input_parser_response_object = {"key" : "value"}
    ....

    return_code = CoreAprsClientInputParserStatus.PARSE_OK
        if there_was_no_error
        else CoreAprsClientInputParserStatus.PARSE_ERROR
    input_parser_error_message = "my_custom_error_message"
        if there_was_an_error
        else ""
    return  return_code, 
            input_parser_error_message,
            input_parser_response_object
```

## Use of dynamic content for APRS bulletins additional to static bulletin content

Sample code: [`demo_aprs_client_with_dynamic_bulletins.py`](/framework_examples/demo_aprs_client_with_dynamic_bulletins.py)

Class property: `CoreAprsClient.dynamic_aprs_bulletins`

### Introduction

> [!NOTE]
> This is an optional extension; in most cases, you will not need to use this function.

As [described in the framework documentation](configuration_subsections/config_bulletin.md), `core-aprs-framework` can send to the [APRS-IS](https://aprs-is.net/) framework at the user's request. The associated bulletin messages are stored as static content [in the configuration file](configuration_subsections/config_bulletin_messages.md). 

In addition to the static bulletin messages configured in the `core-aprs-client`'s configuration file, it is also possible to send dynamic bulletin messages. These could be, for example, special weather data that is only determined during the runtime of the bot. [mpad](https://www.github.com/joergschultzelutter/mpad) uses this, for example, to send out [hazard warnings from the local German weather service](https://github.com/joergschultzelutter/mpad/blob/master/docs/INSTALLATION.md#program-configuration). In a nutshell: a separate background job will fetch the data and feed it to the class instance which will then include it in the APRS bulletin data. By doing so, static APRS bulletins (taken from the configuration file) and dynamic APRS bulletins (generated during runtime) will be taken into account.

### Terms and conditions

> [!IMPORTANT]
> The ability to send this dynamic data is achieved by assigning a variable of `dict` object to a property of the instantiated class. Adding or changing individual elements of this property is _not_ implemented. Always replace that property's value in full.

The following conditions apply:

* The default value of this separate property is an empty `dict` object; i.e., no dynamic bulletins are configured
* The complete list of bulletins (consisting of static and, if available, dynamic bulletins) is regenerated at each interval of the bulletin routine. Changes that have been made to the property of the instantiated class in the meantime are thus always taken into account.
* To send dynamic bulletins, the function for sending static bulletins (i.e., the contents of the configuration file) [must be activated](configuration_subsections/config_bulletin.md) (`aprsis_broadcast_bulletins` = `true`). It is generally possible _not_ to preassign the static contents of the bulletins and to use only dynamic contents.
* Like static bulletins, dynamic bulletins must meet the requirements of the APRS specification, which are defined [in Chapter 14 of the APRS specifications](https://github.com/wb2osz/aprsspec) (_Messages, Bulletins, and Announcements_).
  * `core-aprs-client` supports dynamic bulletins beginning with the prefix `BLN` or `NWS` and follows the format specifications of the APRS specifications, depending on the selected prefix. 
  * The text content uses ASCII-7 bit and is up to 67 characters long per bulletin. When attempting to transfer longer content or empty content, the corresponding entries are ignored in the same way as static bulletins. A corresponding message is also issued as a warning with `logging.DEBUG` level.
  * Dynamic bulletins are only added to the list of outgoing bulletins if their keys are not part of the static bulletins. If there is a `BLN0` entry in both the static and dynamic data, the static entry always takes precedence, as this data is sent out first.
  * Special characters `{}|~` are automatically removed from the outgoing message by `core-aprs-client` in the same way as static bulletins.
  * Garbage in, garbage out. With great power comes great responsibility.

### Using the dynamic bulletins option

Pseudo code; for a detailed example, please see [demo_aprs_client_with_dynamic_bulletins.py](/framework_examples/demo_aprs_client_with_dynamic_bulletins.py).


#### Main function
```python
if __name__ == "__main__":
    client = CoreAprsClient(
        config_file=configfile,
        log_level=logging.DEBUG,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
    )

    # Create the scheduler object which will handle the updates to our
    # class' dictionary item
    my_scheduler = BackgroundScheduler()

    # Add the scheduler job.
    my_scheduler.add_job(
        make_demo_beacon,
        "interval",
        id="beacondemo",
        minutes=90,
        args=[
            client,
        ],
        max_instances=1,
        coalesce=True,
    )

    # start the scheduler
    my_scheduler.start()

    # As we safely want to remove the scheduler in case of ctrl-c or server shutdown,
    # let's add an exception handler
    try:
        # Activate the APRS client and connect to APRS-IS
        client.activate_client()
    except (KeyboardInterrupt, SystemExit):

        # Pause the scheduler and remove all jobs afterwards.
        my_scheduler.pause()
        my_scheduler.remove_all_jobs()
```

#### Scheduler function

Every 90 minutes, this demo scheduler function will create a dictionary with the static content 

- `key` = `BLN0DEMO`
- `value` = `Hello World`

and pass that data to the class instance's property. Amend this function and add your dynamic bulletin content in a similar manner. For a detailed example, please see [demo_aprs_client_with_dynamic_bulletins.py](/framework_examples/demo_aprs_client_with_dynamic_bulletins.py).

```python
def make_demo_beacon(myclient: CoreAprsClient):
    """
    This is a simple "setter" method which will first generate a dictionary
    with random bulletins and then add them to the target dictionary. It gets called
    by the main program's scheduler job.

    Parameters
    ==========

    Returns
    =======

    """
    myclient.dynamic_aprs_bulletins = {"BLN0DEMO": "Hello World"}
```

## Accessing the program's configuration data

Any number of sections for configuration data can be defined within `core-aprs-client`'s [`custom`](configuration_subsections/config_custom.md) configuration file. The data is read when the class is initialized and made available as an __immutable__ dictionary object.

Any number of custom configuration areas can be created; here too, the name ‘custom_config’ is only a placeholder. Of course, this requires that the framework-specific configuration areas remain unchanged.

> [!NOTE]
> All framework-specific sections of the configuration file begin with the prefix `coac`. I recommend using a different prefix for your own code adjustments.

### Example
##### Configuration file excerpt with two custom config sections

```python
[coac_data_storage]
#
# This is the name of the subdiectory where the program will store the
# APRS message counter file. Location: $cwd/<directory>
# If not present, then the directory will be created by the program
aprs_data_directory = data_files
#
# This is the name of the file that will contain the program's message counter
# If not present, then the file will be created by the program
aprs_message_counter_file_name = core_aprs_client_message_counter.txt

[zzz_custom_config]
#
# This section is deliberately kept empty and can be used for storing your
# individual APRS bot's configuration settings. core-aprs-client` will make
# that data available to you via the class object's `config_data` getter property.
# For further details, please have a look at the program's documentation.

Hello = Welt

[zzz_custom_config2]
#
# This section is deliberately kept empty and can be used for storing your
# individual APRS bot's configuration settings. core-aprs-client` will make
# that data available to you via the class object's `config_data` getter property.
# For further details, please have a look at the program's documentation.

Hello = World
```

##### Demo program

```python
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from input_parser import parse_input_message
from output_generator import generate_output_message

import logging
from pprint import pformat

# Create the CoreAprsClient object. Supply the
# following parameters:
#
# - configuration file name
# - log level (from Python's 'logging' package)
# - function names for both input processor and output generator
#
client = CoreAprsClient(
    config_file="my_config_file.cfg",
    log_level=logging.DEBUG,
    input_parser=parse_input_message,
    output_generator=generate_output_message,
)

print (pformat(client.config_data))
```

##### Output (excerpt)

```
              ....
                                 'aprsis_server_name': 'euro.aprs2.net',
                                 'aprsis_server_port': 14580},
              'coac_testing': {'aprsis_enforce_unicode_messages': False,
                          'aprsis_simulate_send': True},
              'zzz_custom_config': {'hello': 'Welt'},
              'zzz_custom_config2': {'hello': 'World'}})

```
