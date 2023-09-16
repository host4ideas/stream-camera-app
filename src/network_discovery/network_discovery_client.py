from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket, AF_INET, SOCK_DGRAM
from src.utils.constants import PORT, MAGIC

PORT = 50000
# to make sure we don't confuse or get confused by other programs
MAGIC = "acb708ca9ec7911f28430e90bad070e1"


s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
s.bind(('', PORT))

while 1:
    data, addr = s.recvfrom(1024)  # wait for a packet
    if data.decode().startswith(MAGIC):
        print("got service announcement from", data[len(MAGIC):])
