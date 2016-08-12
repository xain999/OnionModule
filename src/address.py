# system imports
import socket

class Address(object):
    def __init__(self, ip, port, ipv6):
        self.ip = ip
        self.port = port
        self.ipv6 = ipv6


def receiveAll(sock, size):
    data = ''

    while size > 0:
        recvd = sock.recv(size)
        size = size - len(recvd)
        data = data + recvd

    return data