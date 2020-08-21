#!/bin/bash
echo "This terminal session will now be used for faking serial input. Feed data through one of the pty shown below and read from the other."
socat -d -d pty,raw,b9600,echo=0 pty,raw,b9600,echo=0