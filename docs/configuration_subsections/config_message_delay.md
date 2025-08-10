# Message Delay Configuration

> [!TIP]
> These settings simply configire artificial delays after a message has been sent. With the exception of the 'acknoledgment' delay, all other delays are ONLY applied if more than one message has to be sent out to the user.

| Config variable             | Type    | Default value        | Description                                                                                                                                                                                                   |
|-----------------------------|---------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `packet_delay_message`      | `float` | `6.0`  (= 6 seconds) | Artificial message delay in seconds for regular APRS messages (e.g. responses to the user). Applied when there are still outgoing messages to be sent to APRS-IS.                                             |
| `packet_delay_ack`          | `float` | `2.0`  (= 2 seconds) | Artificial message delay in seconds after sending out an APRS acknowledgment                                                                                                                                  |
| `packet_delay_grace_period` | `float` | `1.0`  (= 1 seconds) | Artificial message delay grace period in seconds after sending the very last message in a message queue. Applies to regular APRS messages, beacons, and bulletins. Does not apply to message acknowledgments. |
| `packet_delay_beacon`       | `float` | `6.0`  (= 6 seconds) | Artificial message delay in seconds after sending out an APRS beacon and there are still pending beacons in our message list.                                                                                 |
| `packet_delay_bulletin`     | `float` | `6.0`  (= 6 seconds) | Artificial message delay in seconds after sending out an APRS bulletin and there are still pending bulletins in our message list.                                                                             |

The respective section from `core-aprs-client`'s config file lists as follows:

```
#
# delay between messages if more than one message is to be sent to APRS-IS
# Unit of measure: seconds
packet_delay_message = 6.0
#
# packet delay after sending an ackknowledgment
# Unit of measure: seconds
packet_delay_ack = 2.0
#
# packet delay after sending the very last message from a message queue
# applies to regular messages, beacons and bulletins and is used as a grace
# period for not hitting APRS-IS messages too fast after processing a user's
# APRS request
# Unit of measure: seconds
packet_delay_grace_period = 1.0
#
# packet delay after sending a bulletin to APRS-IS and there are still pending
# bulletins in our outgoing message list
# Unit of measure: seconds
packet_delay_bulletin = 6.0
#
# packet delay after sending a beacon to APRS-IS and there are still pending
# bulletins in our outgoing message list
# Unit of measure: seconds
packet_delay_beacon = 6.0
```
