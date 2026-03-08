# Test options

## Table of Contents
<!--ts-->
* [Introduction](#introduction)
* [Option 1: Testing using the `dryrun` option](#option-1-testing-using-the-dryrun-option)
* [Option 2: Testing using the `aprsis_simulate_send` flag](#option-2-testing-using-the-aprsis_simulate_send-flag)
* [Conclusion](#conclusion)
<!--te-->



## Introduction

You have already noticed that `core-aprs-client` provides two types of testing options:

Option 1: Testing using the [`dryrun`](/docs/coreaprsclient_class.md#dryrun_testcall-class-method) class method
Option 2: Testing using the [`aprsis_simulate_send`](/docs/configuration_subsections/config_testing.md) flag

So what is the difference between the two? Let's first take a look at the output of both options; both use the `lorem` demo command code from the provided [framework_examples](/framework_examples) folder:

## Option 1: Testing using the `dryrun` option
```python
2026-03-08 13:20:57,980 - demo_dryrun -INFO - Starting demo module: dryrun
2026-03-08 13:20:57,980 - demo_dryrun -INFO - This is a demo APRS client which performs an offline dry-run on a given APRS message/APRS callsign combination.
2026-03-08 13:20:57,982 - client_utils -ERROR - 'aprsis_tocall' is still set to default config; change config file ASAP
2026-03-08 13:20:57,982 - client_utils -ERROR - 'aprsis_callsign' is still set to default config; change config file ASAP
2026-03-08 13:20:57,983 - CoreAprsClient -INFO - Activating dryrun testcall...
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - input_parser: Parsing message 'lorem' for callsign 'DF1JSL-1'
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - Parsed message:
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - {'command_code': 'loremipsum', 'from_callsign': 'DF1JSL-1'}
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - return code: CoreAprsClientInputParserStatus.PARSE_OK
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - output_generator: Running Output Processor build ...
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - Output Generator response=True, message:
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
2026-03-08 13:20:57,984 - CoreAprsClient -INFO - Output generator status successful; building outgoing messages ...
2026-03-08 13:20:57,985 - CoreAprsClient -INFO - ['Lorem ipsum dolor sit amet, consetetur sadipscing elitr,    (01/11)',
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

## Option 2: Testing using the `aprsis_simulate_send` flag

```python
2026-03-08 13:14:31,001 - CoreAprsClient -INFO - Starting APRS-IS callback consumer
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - Received raw_aprs_packet: {'raw': 'DF1JSL-4>APOSB,TCPIP*,qAS,DF1JSL::COAC     :lorem{00008', 'from': 'DF1JSL-4', 'to': 'APOSB', 'path': ['TCPIP*', 'qAS', 'DF1JSL'], 'via': 'DF1JSL', 'addresse': 'COAC', 'format': 'message', 'message_text': 'lorem', 'msgNo': '00008'}
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - Preparing acknowledgment receipt
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - Simulating acknowledgment receipt: COAC>APRS::DF1JSL-4 :ack00008
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - Input parser result: CoreAprsClientInputParserStatus.PARSE_OK
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - {'from_callsign': 'DF1JSL-4', 'command_code': 'loremipsum'}
2026-03-08 13:14:53,186 - client_aprs_communication -INFO - Finalizing and sending APRS messages...
2026-03-08 13:14:53,186 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :Lorem ipsum dolor sit amet, consetetur sadipscing elitr,    (01/11){AO'
2026-03-08 13:14:59,191 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :sed diam nonumy eirmod tempor invidunt ut labore et dolore  (02/11){AP'
2026-03-08 13:15:05,194 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :magna aliquyam erat, sed diam voluptua. At vero eos et      (03/11){AQ'
2026-03-08 13:15:11,198 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :accusam et justo duo dolores et ea rebum. Stet clita kasd   (04/11){AR'
2026-03-08 13:15:17,202 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :gubergren, no sea takimata sanctus est Lorem ipsum dolor    (05/11){AS'
2026-03-08 13:15:23,205 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing (06/11){AT'
2026-03-08 13:15:29,205 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :elitr, sed diam nonumy eirmod tempor invidunt ut labore et  (07/11){AU'
2026-03-08 13:15:35,205 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :dolore magna aliquyam erat, sed diam voluptua. At vero eos  (08/11){AV'
2026-03-08 13:15:41,207 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :et accusam et justo duo dolores et ea rebum. Stet clita     (09/11){AW'
2026-03-08 13:15:47,209 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :kasd gubergren, no sea takimata sanctus est Lorem ipsum     (10/11){AX'
2026-03-08 13:15:53,211 - client_aprs_communication -DEBUG - Simulating response message 'COAC>APRS::DF1JSL-4 :dolor sit amet.                                             (11/11){AY'
```

## Conclusion

The `dryrun` functions perform the same functions as the real APRS bot code. However, the following are missing:

- the generation of the final outgoing APRS messages
- as well as all waiting cycles that are otherwise taken into account by the bot.
- In addition, all testing takes place offline; the test code does not have to establish a connection to APRS-IS first.

If, on the other hand, the `aprsis_simulate_send` flag is used, then
- a connection to APRS-IS must be established
- The bot uses all stored wait cycles; therefore, tests take correspondingly longer.
- Write operations are performed on the APRS message counter file.

For initial tests, using the `dryrun` functions is sufficient and represents the fastest option for testing. Final tests can then be performed with the support of the `aprsis_simulate_send` flag.
