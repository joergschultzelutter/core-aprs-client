# Custom Configuration

> [!TIP]
> Custom content. You can add your very own configuration here - `core-aprs-client` will make that data available to you via the class object's `config_data` 'getter' property. 

Example:

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

    # This will output the framework's configuration file content,
    # including any any content that is specific to your very own program.
    print(pformat(client.config_data))
```

> [!WARNING]
> The config_data property is deliberately provided as an __immutable__ object. Any attempt to modify it will result in a program error.


The respective section from `core-aprs-client`'s config file lists as follows:

```
[custom_config]
#
# This section is deliberately kept empty and can be used for storing your
# individual APRS bot's configuration settings. core-aprs-client` will make
# that data available to you via the class object's `config_data` getter property.
# For further details, please have a look at the program's documentation.
```

> [!INFORMATION]
> Any number of custom configuration areas can be created; here too, the name ‘custom_config’ is only a placeholder. Of course, this requires that the framework-specific configuration areas remain unchanged.
