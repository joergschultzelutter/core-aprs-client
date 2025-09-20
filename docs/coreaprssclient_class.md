# `CoreAprsClient` class

The `CoreAprsClient` class is responsible for the communication between the local APRS bot and APRS-IS. Import the class via

    from CoreAprsClient import CoreAprsClient

## Class Constructor

```
class CoreAprsClient:
    config_file: str
    log_level: int
    input_parser: types.FunctionType
    output_generator: types.FunctionType

    def __init__(
        self,
        config_file: str,
        input_parser: types.FunctionType,
        output_generator: types.FunctionType,
        log_level: int = logging.INFO,
    ):
```

### Parameter

| Field Name         | Description                                                                                 | Field Type |
|--------------------|---------------------------------------------------------------------------------------------|------------|
| `config_file`      | `core_aprs_client`'s configuration file; see [this documentation section](configuration.md) | `str`      |
| `input_parser`     | function name of the external input processor                                               | `function` |
| `output_generator` | function name of the external output generator                                              | `function` |
| `log_level`        | Log level from Python's `logging` function. Default: `logging.INFO`                         | `enum`     |

## `activate_client` method

This method is responsible for the communication between the local APRS bot and APRS-IS. It has no parameters. Full APRS bot client example:

    from CoreAprsClient import CoreAprsClient
    
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

## `dryrun_testcall` method

This method can be used for offline testing. There will be no data exchange between APRS-IS and the bot.

Dryrun code example:

    from CoreAprsClient import CoreAprsClient
    
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

### Parameter

| Field Name      | Description                                                    | Field Type |
|-----------------|----------------------------------------------------------------|------------|
| `message_text`  | The APRS message that we are supposed to process.              | `str`      |
| `from_callsign` | Name of the callsign which has sent us the (simulated) message | `str`      |

### Sample output

This is the sample output for the `lorem` keyword from the `sample_aprs_client` provided with this repository:

```
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

Unlike the `output_generator` which either provides a success/failure scenario, the `input_processor` supports _three_ return codes. Your custom `input_processor` code needs to import those via

    from CoreAprsClient import CoreAprsClientInputParserStatus

Valid values:

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

> [!NOTE]
> `PARSE_IGNORE` should _only_ be used for cases where your custom input processor has implemented e.g. a dupe check that is _additional_ to `core-aprs-client`s dupe check and you don't want to trigger ANY response to the user's inquiry. In any other case, use `PARSE_ERROR` and return a proper response message to the user.

### `input_processor` return code sample

    from CoreAprsClient import CoreAprsClientInputParserStatus

    def process_the_input():
        ....
        do some processing
        my_data_structure = {"key" : "value}
        ....

        return_code = CoreAprsClientInputParserStatus.PARSE_OK if there_was_no_error else CoreAprsClientInputParserStatus.PARSE_ERROR
        return return_code, my_data_structure