# system imports
import socket
import struct
import threading
import sys

#user imports
from socketHelper import recv_all
from address import *

class Peer(object):
    def __init__(self, ip, port, ipv6, hostKey):
        self.address = Address(ip, port, ipv6)
        self.key = hostKey

class RPSConnectionType(enumerate):
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
        self.query = struct.pack('!HH', 4, RPSConnectionType.RPS_QUERY)

        self.lock = threading.Lock()

    def getRandomPeer(self):
        #TODO: check of socket is connected

        with self.lock:
            self.sock.sendall(self.query)

            rawData = self.sock.recv(2)
            size = struct.unpack('!H', rawData[0:2])[0]
            rawData = recv_all(self.sock, size - 2)
            id = struct.unpack('!H', rawData[:2])[0]
            if id != RPSConnectionType.RPS_PEER:
                print("Cannot get Peer")
                sys.exit(1)
            
            port = struct.unpack('!H', rawData[2:4])[0]
            ip = None
            key = ''

            if self.isIPv6:
                ip = socket.inet_ntop(socket.AF_INET6, str(rawData[6:22]))
                key = str(rawData[22:])
            else:
                ip = socket.inet_ntop(socket.AF_INET, str(rawData[6:10]))
                key = str(rawData[10:])

            return Peer(ip, port, self.isIPv6, key)
        

