# Message Delay Configuration

> [!TIP]
> These settings simply configire artificial delays after a message has been sent. With the exception of the 'acknoledgment' delay, all other delays are ONLY applied if more than one message has to be sent out to the user.

| Config variable        | Type    | Default value        | Description                                                                      |
|------------------------|---------|----------------------|----------------------------------------------------------------------------------|
| `packet_delay_message` | `float` | `6.0`  (= 6 seconds) | Artificial message delay in seconds for regular APRS messages (e.g. responses to the user). |
| `packet_delay_other`   | `float` | `6.0`  (= 6 seconds) | Artificial message delay in seconds after sending out APRS bulletins and/or beacons.        |
| `packet_delay_ack`     | `float` | `2.0`  (= 2 seconds) | Artificial message delay in seconds after sending out an APRS acknowledgment     |

The respective section from `core-aprs-client`'s config file lists as follows:

```
[message_delay]
#
# delay between messages if more than one message is to be sent to APRS-IS
# Unit of measure: seconds
packet_delay_message = 6.0
#
# packet delay after sending a bulletin or beacon
# Unit of measure: seconds
packet_delay_other = 6.0
#
# packet delay after sending an ackknowledgment
# Unit of measure: seconds
packet_delay_ack = 2.0
```
