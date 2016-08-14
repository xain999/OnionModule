# system imports
import socket
import uuid

from enum import Enum


class UDPMsgType(Enum):
    FWD = 590
    USE = 591

class SocketManager(object):
    def __init__(self, packetSize):
        self.sockets = {}
        self.packetCount = {}
        self.packetCountTotal = {}
        self.packetAssembler = {}
        self.packetSize = packetSize
        self.isIPv6 = {}

    def addSocket(self, address):
        if address.ipv6:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.bind((address.ipv6, address.port))
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((address.ip, address.port))

        socket_id = uuid.uuid4()
        self.sockets[socket_id] = sock
        return socket_id

    def removeSocket(self, port):
        if self.sockets[port] != None:
            sock = self.sockets[port]
            sock.close()
            self.sockets.remove(sock)
            self.sockets[port] = None

    def _forwardMessage(self, rawData, sock):
        port = struct.unpack('!H, rawData[:2])
        ip = None
        if self.isIPv6:
            ip = socket.inet_ntop(socket.AF_INET6, rawData[4:20])
            rawData = rawData[20:]
        else:
            ip = socket.inet_ntop(socket.AF_INET, rawData[4:8])
            rawData = rawData[8:]

        sock.sendto(rawData, (ip, port))

    def _assembleAndRead(self, rawData, ui):
        size = struct.unpack('!H, rawData[:2]) - 2
        pktId = struct.unpack('!H, rawData[2:4])
        pktCount = struct.unpack('!H, rawData[4:6])
        pktNo = struct.unpack('!H, rawData[4:6])
        data = rawData[8:size - 8]

        if self.packetCountTotal[pktId] == None:
            self.packetCountTotal[pktId] = pktCount
            self.packetCount[pktId] = 1
            packetData = {}
            packetData[pktNo] = data
            self.packetAssembler[pktId] = packetData
        else:
            self.packetCount[pktId] += 1
            packetData = self.packetAssembler[pktId]
            packetData[pktNo] = data
            if self.packetCountTotal[pktId] == self.packetCount[pktId]:
                data = ''
                count = self.packetCountTotal[pktId] + 1
                for i in range(1, count):
                    data += packetData[i]
                
                self.packetCountTotal[pktId] = None
                self.packetCount[pktId] = None
                self.packetAssembler[pktId] = None

                ui.send(data)

    def update(self, address, ui):
        readable, writable, exceptional = select.select(self.sockets, [], self.sockets)

        for s in readable:
            rawData = s.recv(self.packetSize)
            id = struct.unpack('!H, rawData[:2])
            
            if id == UDPMsgType.FWD:
                self._forwardMessage(rawData[2:], s)
            elif id == UDPMsgType.USE:
                self._assembleAndRead(rawData[2:], ui)
            