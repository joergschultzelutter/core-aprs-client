# Framework & Sample Client Installation

# Introduction

Although `core-aprs-client` is provided as a Python package, you should follow the steps below to familiarize yourself with the program:

- Clone repository
- Install a Python 3.11+ virtual environment and activate it
- `cd sample_aprs_client`
- `pip install -r requirements.txt` (this will install the sample client's required Python packages)
- Follow the configuration instructions and change the [mandatory configuration file sections](https://github.com/joergschultzelutter/core-aprs-client/blob/23-implement-functoolspartial/docs/configuration.md#mandatory-configuration-file-sections)
- run the `sample_aprs_client.py`
- Send an APRS message to the bot's callsign
- Enjoy

Whenever necessary, you can install work-in-progress packages straight via GitHub:

```
git+https://github.com/joergschultzelutter/core-aprs-client@this-is-my-branch-name#egg=core-aprs-client
```
