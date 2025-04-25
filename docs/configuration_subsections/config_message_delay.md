# Message Delay

> [!TIP]
> These settings simply configire artificial delays after a message has been sent. With the exception of the 'acknoledgment' delay, all other delays are ONLY applied if more than one message has to be sent out to the user.

- ```packet_delay_message``` - artificial message delay for regular APRS messages (e.g. responses to the user). Default = 6.0 seconds 
- ```packet_delay_other``` - artificial message delay after sending out APRS bulletins and/or beacons. Default = 6.0 seconds 
- ```packet_delay_ack``` - artificial message delay after sending out an APRS acknowledgment. Default = 2.0 seconds 

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
