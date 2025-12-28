# Framework & Sample Client Installation

# Introduction

Although `core-aprs-client` is provided [as a Python package](https://pypi.org/project/core-aprs-client/), you should follow the steps below to familiarize yourself with the framework and run first tests with the provided sample code:

- Clone this repository
- Install a Python 3.11+ virtual environment and activate it
- Open the [framework_examples](/framework_examples) directory
- `pip install -r requirements.txt` (this will install the sample clients' required Python packages)
- Follow the configuration instructions and change the [mandatory configuration file sections](/docs/configuration.md#mandatory-configuration-file-sections)
- Run one of the provided demo clients, e.g.the [`demo_aprs_client.py`](/framework_examples/demo_aprs_client.py) bot
- Send an APRS message to your bot's callsign
- Enjoy

For further details on the provided framework examples, please see [this document](/framework_examples/README.md).