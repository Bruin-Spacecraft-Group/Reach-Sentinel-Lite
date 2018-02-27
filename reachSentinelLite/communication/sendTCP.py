import socket
#wlan0 address of raspberry pi
#TCP_IP = '10.10.10.194'
#TCP_PORT = 5005
BUFFER_SIZE = 1024

def initSocket(TCP_IP, TCP_PORT):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((TCP_IP, TCP_PORT))
	return sock

def sendPacket(sock, data):
	sock.send(data)

def killSocket(sock):	
	sock.close()