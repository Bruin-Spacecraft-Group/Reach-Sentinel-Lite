import serial
import time
import socket

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

print(("connected to: " + ser.portstr))

with open('output.txt', 'w+') as output:
    output.write("")

UDP_IP = "192.168.56.101"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

count = 0;
while True:
    data = ser.readline()
    print(( str(count) + ":" + data ))
    output = open('output.txt', 'a+')
    output.write(data + '\n')
    sock.sendto(data, (UDP_IP, UDP_PORT))
    count += 1
    time.sleep(0.1)

ser.close()