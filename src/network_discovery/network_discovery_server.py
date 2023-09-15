from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from time import sleep
from utils.constants import PORT, MAGIC


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
