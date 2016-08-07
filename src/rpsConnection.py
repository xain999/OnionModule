# system imports
import socket
import struct

#user imports
from address import *

class RandomPeer(object):
    def __init__(self, ip, port, ipv6, hostKey):
        self.address = Address(ip, port, ipv6)
        self.key = hostKey

class RPSConnection(object):
    def __init__(self, address):
        self.RPS_QUERY = 540
        self.RPS_PEER = 541
        
        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.connect((address.ip, address.port))

        self.query = struct.pack('>hh', 4, self.RPS_QUERY)

    def getRandomPeer(self):
        #TODO: check of socket is connected
        check = self.sock.send(self.query)

        if check != len(self.query):
            raise Exception('socket sent error!')

        rawData = self.sock.recv(2)
        size = struct.unpack('>h', rawData[0:2])
        rawData = self.sock.recv(size[0] - 2)
        id = struct.unpack('>h', rawData[:2])
        if id[0] != self.RPS_PEER:
            return None
        
        port = struct.unpack('>h', rawData[2:4])
        ip = None
        ipv6 = False
        key = ''

        if size[0] == 524:
            ip = socket.inet_ntop(socket.AF_INET, rawData[6:10])
            ipv6 = False
            key = rawData[10:]

        elif size[0] == 536:
            ip = socket.inet_ntop(socket.AF_INET6, rawData[6:22])
            ipv6 = True
            key = rawData[22:]
        else:
            return None

        return RandomPeer(ip, port[0], ipv6, key)
        

