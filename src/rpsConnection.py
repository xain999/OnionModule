# system imports
import socket
import struct
import threading

#user imports
from address import *

class Peer(object):
    def __init__(self, ip, port, ipv6, hostKey):
        self.address = Address(ip, port, ipv6)
        self.key = hostKey

class RPSConnectionType(Enum):
    RPS_QUERY = 540
    RPS_PEER = 541

class RPSConnection(object):
    def __init__(self, address, isIPv6):
        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.connect((address.ip, address.port))
        self.isIPv6 = isIPv6
        self.query = struct.pack('>hh', 4, RPSConnectionType.RPS_QUERY)

        self.lock = threading.Lock()

    def getRandomPeer(self):
        #TODO: check of socket is connected

        with self.lock:
            check = self.sock.sendall(self.query)

            if check != len(self.query):
                raise Exception('socket sent error!')

            rawData = self.sock.recv(2)
            size = struct.unpack('>h', rawData[0:2])
            rawData = self.sock.recv(size[0] - 2)
            id = struct.unpack('>h', rawData[:2])
            if id[0] != RPSConnectionType.RPS_PEER:
                return None
            
            port = struct.unpack('>h', rawData[2:4])
            ip = None
            key = ''

            if self.isIPv6:
                ip = socket.inet_ntop(socket.AF_INET6, rawData[6:22])
                key = rawData[22:]
            else:
                ip = socket.inet_ntop(socket.AF_INET, rawData[6:10])
                key = rawData[10:]

            return Peer(ip, port[0], self.isIPv6, key)
        

