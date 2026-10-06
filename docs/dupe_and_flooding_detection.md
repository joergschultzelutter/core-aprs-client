# Dupe Detection and Request Flooding Detection

`core-aprs-client` has two separate configuration sections that are related to detecting duplicate requests:

- [config_dupe_detection.md](./configuration_subsections/config_dupe_detection.md) is the dupe handler for ALL requests to the bot framework, regardless of whether they have been successful or not. 
- [config_flooding.md](./configuration_subsections/config_flooding.md) is the dupe handler for UNSUCCESSFUL requests to the bot framework which would generate a default error message (see `aprs_input_parser_default_error_message` from [config_client.md](./configuration_subsections/config_client.md)).

Let's have a look at the difference between those two dupe mechanisms:

## [config_dupe_detection.md](./configuration_subsections/config_dupe_detection.md)

This configuration section detects all kind of duplicate requests to the bot framework, regardless of whether these requests have been successful or not. Due to the nature of APRS-IS, the very same request might get received more than once by the bot within a short period of time. [config_dupe_detection.md](./configuration_subsections/config_dupe_detection.md) detects all of those duplicate requests to the framework and ignores those requests. Note that this also mean that you will not be able to send the very same valid request to the bot within the time span defined in [config_dupe_detection.md](./configuration_subsections/config_dupe_detection.md).

Example - let's assume that the valid framework command `sayhello` is received by the bot more than once and that both messages have the same message ID number:

```
2026-10-04 19:33:56,925 - CoreAprsClient -DEBUG - Establishing connection to APRS-IS...
2026-10-04 19:33:56,925 - inet -INFO - Attempting connection to euro.aprs2.net:14580
2026-10-04 19:33:56,959 - inet -INFO - Connected to ('2001:41d0:801:2000::593b', 14580, 0, 0)
2026-10-04 19:33:56,997 - inet -INFO - Sending login information
2026-10-04 19:33:57,023 - inet -INFO - Login successful
2026-10-04 19:33:57,023 - CoreAprsClient -DEBUG - Established the connection to APRS-IS
2026-10-04 19:33:57,023 - CoreAprsClient -INFO - Starting APRS-IS callback consumer

>>> first request with msg ID 00014 is received and processed

2026-10-04 19:34:25,882 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :sayhello{00014', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'sayhello', 'msgNo': '00014'}
2026-10-04 19:34:25,882 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 19:34:25,882 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00014
2026-10-04 19:34:27,886 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_OK
2026-10-04 19:34:27,886 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': 'sayhello'}
2026-10-04 19:34:27,886 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 19:34:27,887 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Hello World{CC'

>>> second request with the same msg id 00014 is received and ignored as the message (read: this is the same request as the first one)

2026-10-04 19:34:33,305 - client_aprs_communication -DEBUG - DUPLICATE APRS PACKET - this message is still in our decaying message cache
2026-10-04 19:34:33,306 - client_aprs_communication -DEBUG - Ignoring duplicate APRS packet raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :sayhello{00014', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'sayhello', 'msgNo': '00015'}
```

As a result, you will only receive ONE response from the bot. The second one gets ignored and does not even get acknowledged by the bot.

Now, assume that the very same command `sayhello` is again sent to the bot more than once. But this time, the message numbers differ - meaning that actually, someone did send that request to the bot twice:

```
026-10-04 19:52:24,525 - inet -INFO - Sending login information
2026-10-04 19:52:24,546 - inet -INFO - Login successful
2026-10-04 19:52:24,546 - CoreAprsClient -DEBUG - Established the connection to APRS-IS
2026-10-04 19:52:24,546 - CoreAprsClient -INFO - Starting APRS-IS callback consumer

>>> receiving first message with message id 00016

2026-10-04 19:52:37,992 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :sayhello{00016', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'sayhello', 'msgNo': '00016'}
2026-10-04 19:52:37,992 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 19:52:37,992 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00016
2026-10-04 19:52:39,995 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_OK
2026-10-04 19:52:39,996 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': 'sayhello'}
2026-10-04 19:52:39,996 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 19:52:39,996 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Hello World{CD'

>>> receiving second message with message ID 00017

2026-10-04 19:52:44,250 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :sayhello{00017', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'sayhello', 'msgNo': '00017'}
2026-10-04 19:52:44,250 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 19:52:44,250 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00017
2026-10-04 19:52:46,256 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_OK
2026-10-04 19:52:46,256 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': 'sayhello'}
2026-10-04 19:52:46,256 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 19:52:46,257 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Hello World{CE'
```

As both messages have different message ID's (00016 and 00017), these messages are NOT considered as duplicates and will get processed by the bot - even though their message body contains the very same content. Note that this filter is obviously only possible when sending a message with a message ID - if you send APRS requests without message ID, `core-aprs-client` can neither ACK those requests nor it can distinguish request A from request B.

> [!TIP]
> If necessary, you can remove the message ID as distinguishing element from the dupe detection process by setting [config_dupe_detection.md](./configuration_subsections/config_dupe_detection.md)'s `dupe_check_ignore_msgid` configuration to `true`. If you do so, `core-aprs-client` will perform the dupe check only on the user`s call sign and the message body.

## [config_flooding.md](./configuration_subsections/config_flooding.md)

This configuration section detects failed requests which are answered by the bot via [config_client.md](/docs/configuration_subsections/config_client.md)'s `aprs_input_parser_default_error_message` setting. Assume that someone sends the same erroneous command to the bot over and over again - which would result in receiving the very same bot error message over and over again.

The flooding detection prevents this scenario my stopping any standard responses after a configurable number of erroneous requests has been reached. In this particular example, that threshold is set to the value of "3" - meaning that if the bot has generated two standard bot responses to the user, the third one will indicate a notification to the user that there won't be any further "Invalid command" communication from the bot.

```
2026-10-04 20:02:04,318 - inet -INFO - Sending login information
2026-10-04 20:02:04,347 - inet -INFO - Login successful
2026-10-04 20:02:04,347 - CoreAprsClient -DEBUG - Established the connection to APRS-IS
2026-10-04 20:02:04,347 - CoreAprsClient -INFO - Starting APRS-IS callback consumer

>>> first erroneous request is received

2026-10-04 20:02:14,241 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :hurz{00018', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'hurz', 'msgNo': '00018'}
2026-10-04 20:02:14,242 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 20:02:14,242 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00018
2026-10-04 20:02:16,247 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_ERROR
2026-10-04 20:02:16,247 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': ''}
2026-10-04 20:02:16,248 - client_aprs_communication -DEBUG - Unable to process APRS packet {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :hurz{00018', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'hurz', 'msgNo': '00018'}
2026-10-04 20:02:16,248 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 20:02:16,248 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Invalid command; check documentation at                     (01/02){CF'
2026-10-04 20:02:22,253 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :https://github.com/joergschultzelutter/core-aprs-client     (02/02){CG'

>>> second erroneous request is received

2026-10-04 20:02:32,410 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :wurz{00019', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'wurz', 'msgNo': '00019'}
2026-10-04 20:02:32,410 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 20:02:32,410 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00019
2026-10-04 20:02:34,414 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_ERROR
2026-10-04 20:02:34,414 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': ''}
2026-10-04 20:02:34,414 - client_aprs_communication -DEBUG - Unable to process APRS packet {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :wurz{00019', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'wurz', 'msgNo': '00019'}
2026-10-04 20:02:34,414 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 20:02:34,415 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Invalid command; check documentation at                     (01/02){CH'
2026-10-04 20:02:40,419 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :https://github.com/joergschultzelutter/core-aprs-client     (02/02){CI'

>>> third erroneous request is received. Note that three requests is the flooding detection threshold limit from the framework's config file, so we will receive a different response from the framework

2026-10-04 20:02:44,452 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :hurz{00020', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'hurz', 'msgNo': '00020'}
2026-10-04 20:02:44,452 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 20:02:44,452 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00020
2026-10-04 20:02:46,456 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_ERROR
2026-10-04 20:02:46,456 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': ''}
2026-10-04 20:02:46,457 - client_aprs_communication -DEBUG - Unable to process APRS packet {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :hurz{00020', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'hurz', 'msgNo': '00020'}
2026-10-04 20:02:46,457 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
>>> different framework response starts here
2026-10-04 20:02:46,457 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :Invalid command. Further error msgs will get suppressed in  (01/02){CJ'
2026-10-04 20:02:52,461 - client_aprs_communication -DEBUG - Sending response message 'COAC>APRS::DF1JSL-4 :order to prevent message flooding                           (02/02){CK'
2026-10-04 20:03:00,972 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :blahblahblah{00021', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'blahblahblah', 'msgNo': '00021'}
2026-10-04 20:03:00,972 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-10-04 20:03:00,972 - client_aprs_communication -DEBUG - Sending acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00021
2026-10-04 20:03:02,976 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_ERROR
2026-10-04 20:03:02,976 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': ''}

>>> fourth erroneous request has been received. Note: number of erroneous requests has exceeded the configured threshold, meaning that we won't send anything back to the user. The request itself has been ACKed, though.

2026-10-04 20:03:02,976 - client_aprs_communication -DEBUG - Unable to process APRS packet {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :blahblahblah{00021', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'blahblahblah', 'msgNo': '00021'}
2026-10-04 20:03:02,976 - client_aprs_communication -DEBUG - Finalizing and sending APRS messages...
2026-10-04 20:03:02,976 - client_aprs_communication -DEBUG - APRS message is empty; nothing to send...
```

The bot will continue to send those default error messages if:

- the callsign/counter entry from the flooding prevention dictionary has expired OR
- the `aprs_flooding_counter_reset_for_good_msgs` sweitch has been set and at least one successful request has been processed by the bot.
