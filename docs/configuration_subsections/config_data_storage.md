# Data Storage

> [!TIP]
> Configuration settings for the program`s data files, such as the file that holds the APRS message counter.

This configuration section contains two settings:

- ```aprs_data_directory``` describes the name of the directory which will contain the program's data files. It is always relative to the current directory, meaning that if your current directory is ```/my/current/directory``` and ```aprs_data_directory = data_files```, then the directory used for storing data files is ```/my/current/directory/data_files```. Note: The bot will create the directory if it does not exist.
- ```aprs_message_counter_file_name```is the name of the file which contains the APRS bot's message counter. It resides in the ```aprs_data_directory``` subdirectory. ```core-aprs-client```will create this file in case it does not exist.

```
[data_storage]
#
# This is the name of the subdiectory where the program will store the
# APRS message counter file. Location: $cwd/<directory>
# If not present, then the directory will be created by the program
aprs_data_directory = data_files
#
# This is the name of the file that will contain the program's message counter
# If not present, then the file will be created by the program
aprs_message_counter_file_name = core_aprs_client_message_counter.txt
```
