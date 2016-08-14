# system imports
import select
import thread

#user imports
from socketHelper import recv_all
from rpsConnection import *


class UIConnectionType(enumerate):
    ONION_TUNNEL_BUILD = 560
    ONION_TUNNEL_READY = 561
    ONION_TUNNEL_INCOMING = 562
    ONION_TUNNEL_DESTROY = 563
    ONION_TUNNEL_DATA = 564
    ONION_ERROR = 565
    ONION_COVER = 566


class UIConnection(object):
    def __init__(self, address, isIPv6, hops, rps):
        self.isIPv6 = isIPv6
        self.hops = hops
        self.rps = rps

        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address.ip, address.port))
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()
        self.key = ''

    def _buildTunnel(self, onion, rawData):
        port = struct.unpack('!H', rawData[2:4])[0]
        ip = None
        self.key = None

        if self.isIPv6:
            ip = socket.inet_ntop(socket.AF_INET6, str(rawData[4:20]))
            self.key = str(rawData[20:])
        else:
            ip = socket.inet_ntop(socket.AF_INET, str(rawData[4:8]))
            self.key = str(rawData[8:])
        
        destPeer = Peer(ip, port, self.isIPv6, self.key)
        randomPeers = []
        for i in range(self.hops):
            randomPeers.append(self.rps.getRandomPeer())
        onion.buildTunnel(destPeer, randomPeers)
        print "Tunnel built"

    def _destroyTunnel(self, onion, rawData):
        tunnelId = struct.unpack('!L', (rawData[:4]))[0]
        #onion.destroyTunnel(tunnelId)
        print "tunnel destroyed"
        
    def _coverTraffic(self, onion, rawData):
        print "cover traffic"
        size = struct.unpack('!H', (rawData[:2]))[0]
        onion.sendCoverTraffic()
        print "traffic sent"

    def tunnelReady(self, tunnelId):
        packet = struct.pack('!HL', UIConnectionType.ONION_TUNNEL_READY, tunnelId)
        packet += str.encode(self.key)
        length = len(packet) + 2
        packet = packet + struct.pack('!H', length)
        self.connection.sendall(packet)

    def tunnelIncoming(self, tunnelId, key):
        packet = struct.pack('!HL', UIConnectionType.ONION_TUNNEL_INCOMING, tunnelId)
        packet += key
        length = len(packet) + 2
        packet = packet + struct.pack('!H', length)
        self.connection.sendall(packet)

    def sendDataToUI(self, tunnelId, data):
        packet = struct.pack('!HL', UIConnectionType.ONION_TUNNEL_DATA, tunnelId)
        packet += data
        length = len(packet) + 2
        packet = packet + struct.pack('!H', length)
        self.connection.sendall(packet)
        
    def _sendData(self, onion, data):
        tunnelId = struct.unpack('!H', rawData[:4])[0]
        data = data[:4]
        onion.send(tunnelId, data)

    def checkForData(self):
        readable, writable, exceptional = select.select([ self.connection ], [], [ self.connection ])

        if len(exceptional) > 0:
            print "UI Module connection failed"
            return True

        if len(readable) == 1:
            rawData = self.connection.recv(4)
            if rawData:
                size = struct.unpack('!H', rawData[:2])[0]
                id = struct.unpack('!H', rawData[2:4])[0]
                rawData = recv_all(self.connection, size - 4)

                print("rawData : " + str(rawData))
                onion = 'onion'

                #TODO: Do threading here
                if id == UIConnectionType.ONION_TUNNEL_BUILD:
                    print ("build tunnel")
                    self._buildTunnel(onion, rawData)
                elif id == UIConnectionType.ONION_TUNNEL_DESTROY:
                    print("tunnel destroy")
                    self._destroyTunnel(onion, rawData)
                elif id == UIConnectionType.ONION_TUNNEL_DATA:
                    print("onion data")
                    self._sendData(onion, rawData)
                elif id == UIConnectionType.ONION_COVER:
                    print("cover traffic")
                    self._coverTraffic(onion, rawData)
            else:
                print "UI Module Disconnected"
                exit(1)

        return False
            

