import socket
import time
#wlan0 address of raspberry pi
UDP_IP = "192.168.56.101"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
count = 1

t = time.time()
dt = time.time()
while (dt-t) <= 1:
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	print(count)
	count +=1
	dt = time.time()