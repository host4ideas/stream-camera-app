from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket, AF_INET, SOCK_DGRAM
from utils.constants import PORT, MAGIC

s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
s.bind(('', PORT))

while 1:
    data, addr = s.recvfrom(1024)  # wait for a packet
    if data.decode().startswith(MAGIC):
        print("got service announcement from", data[len(MAGIC):])
