# Reach Data Processing

This is the repository for the data analysis side of project Reach.

The main file is a python script designed to import, process, and then export telemetry data to an external server.


### Prerequisites

Python version: developed with 2.7, may run fine with 3.x

Python libraries used:

```
pySerial
```

Arduino:
paste url: https://adafruit.github.io/arduino-board-index/package_adafruit_index.json into preferences tab of the arduino ide.
From the board manager, install both the arduino SAMD boards and the adafruit SAMD boards.


## Getting Started
Set up the recieve radio (Adafruit Feather M0 in this case) with code to push recieved data packets to the serial port.
Adjust python script to read from the correct port by changing variable SERIAL_PORT.
Adjust upload address to the proper IP adress of the server on current network by changing variable SEND_TO_IP.

Run python ./main.py to launch processing script.

note: the serial port can only be occupied by a single process at a time, therefore upload code to the feather first, then run pyserial code.
