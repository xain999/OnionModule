import socket

class UDPSocket(object):
    def __init__(self, address):
        self.ip = address.ip
        self.port = address.port
        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(ip, port)

    def receive():


class TCPSocketListen(object):
    def __init__(self, address):
        self.ip = address.ip
        self.port = address.port
        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREA)
        self.sock.bind((host, port))