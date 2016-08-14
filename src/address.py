# system imports
import socket

class Address(object):
    def __init__(self, ip, port, ipv6):
        self.ip = ip
        self.port = port
        self.ipv6 = ipv6
