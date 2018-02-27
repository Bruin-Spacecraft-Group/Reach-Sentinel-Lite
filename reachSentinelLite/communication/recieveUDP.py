import socket

#UDP_IP = "169.254.200.27"
UDP_IP = ""
UDP_PORT = 5010

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print("started")
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)