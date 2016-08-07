# system imports
import socket
import struct
from threading import Thread

class UIConnection(object):
    def _threadFunction():
        self.connection, address = sock.accept()

    def __init__(self, address):
        self.RPS_QUERY = 540
        self.RPS_PEER = 541
        self.connection = None

        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.bind((address.ip, address.port))
        self.sock.listen(1)

        self.thread = threading.Thread(target=self._threadFunction).start()

