# system imports
import socket
import struct
import select
from threading import Thread

#user imports
from rpsConnection import *

class OnionMsgType(Enum):
    RELAY_SETUP = 570
    RELAY_CONFIRM = 571
    RELAY_MSG = 572
    RELAY_DESTROY = 573
    RELAY_ERROR = 574
    TUNNEL_REQUEST = 575
    TUNNEL_ACCEPT = 576
    TUNNEL_DECLINE = 577
    TUNNEL_CLOSE = 578

class Onion(object):
    def __init__(self, address, maxConnections, udpManager):
        self.isIPv6 = isIPv6
        self.ip = address.ip
        self.udpManager = udpManager

        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.bind((address.ip, address.port))
        self.server.listen(maxConnections)
        self.input = [ self.server ]
        self.forward = []
        self.forwardMapping = {}
        self.reverse = []
        self.reverseMapping = {}

    def _relaySetup(self, rawData, inSock):
        dstPort = socket.ntohs(rawData[:2])
        key = None
        tunnelId = None
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        if self.isIPv6:
            dstIP = socket.inet_ntop(socket.AF_INET6, rawData[4:20])
            tunnelId = socket.ntohs(rawData[20:24])
            key = rawData[24:]
            sock.connect((dstIP, port))

        else:
            dstIP = socket.inet_ntop(socket.AF_INET, rawData[4:8])
            tunnelId = socket.ntohs(rawData[8:12])
            key = rawData[12:]
            sock.connect((dstIP, port))

        self.input.append(sock)
        self.forward.append(inSock)
        self.forwardMapping[tunnelId] = inSock
        self.reverse.append(sock)
        self.reverseMapping[tunnelId] = sock

        port = self.udpManager.addSocket()

        response = struct.pack('>hhh', OnionMsgType.RELAY_CONFIRM, port, 0)

        if self.isIPv6:
            response += socket.inet_pton(socket.AF_INET6, self.ip)
        else
            response += socket.inet_pton(socket.AF_INET, self.ip)
        
        size = len(response) + 2
        response = socket.htons(size) + response
        inSock.sendall(response)

    def _relayMessage(self, rawData, inSock):
        tunnelId = socket.ntohs(rawData[:4])
        rawData = rawData[4:]
        if inSock in self.forward:
            sock = self.reverseMapping[tunnelId]
            sock.sendall(rawData)
        else
            sock = self.forwardMapping[tunnelId]
            sock.sendall(rawData)

    def _relayDestroy(self, rawData, inSock):
        tunnelId = socket.ntohs(rawData[:4])
        rawData = rawData[4:]
        sock = None

        if len(rawData) > 0:
            if inSock in self.forward:
                sock = self.reverseMapping[tunnelId]
            else
                sock = self.forwardMapping[tunnelId]

        sock.sendall(rawData)
        self.input.remove(sock)
        self.forward.remove(sock)
        self.reverse.remove(sock)
        self.forwardMapping[tunnelId] = None
        self.reverseMapping[tunnelId] = None
        

    def _relayError(self, ui):
        

    def _tunnelRequest(self):

    def _tunnelClose(self):

    def buildTunnel(self):

    def destroyTunnel(self):

    def sendCoverTraffic(self):

    def update(self)
        readable, writable, exceptional = select.select(input, [], input)

        # Handle inputs
        for s in readable:
            if s is self.server:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                self.inputs.append(connection)

            else:
                rawData = s.recv(4)

                if rawData:
                    size = socket.ntohs(rawData[:2])
                    id = socket.ntohs(rawData[2:4])
                    rawData = s.recv(size - 4)
                    
                    if id == OnionMsgType.RELAY_SETUP:
                        _relaySetup(rawData, s)
                    elif id == OnionMsgType.RELAY_MSG:
                        _relayMessage(rawData, s)
                    elif id == OnionMsgType.RELAY_DESTROY:
                        _relayDestroy(rawData, s)
                    elif id == OnionMsgType.RelayError:
                        _relayError()
                    elif id == OnionMsgType.TUNNEL_REQUEST
                        _tunnelRequest()
                    elif id == OnionMsgType.TUNNEL_CLOSE
                        _tunnelClose()
                    
                    
                else:
                    inputs.remove(s)
                    s.close()