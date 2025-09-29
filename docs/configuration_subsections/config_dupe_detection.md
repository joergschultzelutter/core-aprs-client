# Dupe Detection Configuration

> [!TIP]
> This section of the configuration file sets the [APRS-IS](https://aprs-is.net/) dupe detection parameters. Both parameters do not require any modification. Do not apply changes to these settings unless you are aware of the consequences.

Due to the nature of APRS, we might receive the same APRS message as a resubmission. In order to avoid processing that same message again, `core-aprs-client` provides you with a duplicate message detection. Whenever an ingress APRS message is processed, `core-aprs-client` will first check if that message wasn't already processed within a given time span (`msg_cache_time_to_live`). When still present in that dictionary, such a message is identified as a duplicate and will not get processed again. 

| Config variable          | Type  | Default value     | Description                                                                                                                                                                                                                                                                                                                                                                                             |
|--------------------------|-------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `msg_cache_max_entries`  | `int` | `2160`            | Defines the maximum number of incoming APRS messages that are checked for ingress duplicates.                                                                                                                                                                                                                                                                                                           |
| `msg_cache_time_to_live` | `int` | `3600` (= 1 hour) | Sets the life span for a dupe detection's dictionary entry (unit of measure = seconds). Every time an ingress APRS message is accepted, that entry is added to an internal dictionary. Each dictionary entry gets equipped with an individual life span which is defined by the `msg_cache_time_to_live` parameter. Once that time span has been exceeded, the entry gets removed from that dictionary. |

The respective section from `core-aprs-client`'s config file lists as follows:

```
[dupe_detection]
#
# Internal dupe message cache configuration
#
# maximum number of messages
msg_cache_max_entries = 2160
#
# max time span of dupe detection in seconds (3600 sec = 1 hour)
msg_cache_time_to_live = 3600
```
