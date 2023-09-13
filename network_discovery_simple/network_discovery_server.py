from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from time import sleep
PORT = 50000
MAGIC = "fna349fn"  # to make sure we don't confuse or get confused by other programs


s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # this is a broadcast socket
# get our IP. Be careful if you have multiple network interfaces or IPs
my_ip = gethostbyname(gethostname())

while 1:
    data = MAGIC+my_ip
    s.sendto(data.encode(), ('<broadcast>', PORT))
    print("sent service announcement")
    sleep(5)
