import socket
#wlan0 address of raspberry pi
SET_UDP_IP = "10.10.10.193"
SET_UDP_PORT = 5005
MESSAGE = "Hello, World!"

def initSocket(UDP_IP, UDP_PORT):
	UDP_IP = UDP_IP
	UDP_PORT = UDP_PORT
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 5005))
	return sock

def sendPacket(sock, data):
	sock.sendto(data, (UDP_IP, UDP_PORT))

def killSocket(sock):	
	sock.close()