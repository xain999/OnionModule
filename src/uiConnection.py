# system imports
import socket
import select
from threading import Thread

#user imports
from rpsConnection import *


class UIConnectionType(Enum):
    ONION_TUNNEL_BUILD = 560
    ONION_TUNNEL_READY = 561
    ONION_TUNNEL_INCOMING = 562
    ONION_TUNNEL_DESTROY = 563
    ONION_TUNNEL_DATA = 564
    ONION_ERROR = 565
    ONION_COVER = 566


class UIConnection(object):
    def __init__(self, address, isIPv6, hops):
        self.isIPv6 = isIPv6
        self.hops = hops

        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address.ip, address.port))
        self.sock.listen(1)
        self.connection, self.address = self.sock.accept()

    def _buildTunnel(self, onion, rps, rawData):
        pass
        """
        port = socket.ntohs(rawData[2:4])
        ip = None
        key = ''

        if self.isIPv6:
            ip = socket.inet_ntop(socket.AF_INET6, rawData[4:20])
            key = rawData[20:]
        else:
            ip = socket.inet_ntop(socket.AF_INET, rawData[4:8])
            key = rawData[8:]
        
        destPeer = Peer(ip, port, self.IPv6, key)
        randomPeers = []
        for i in self.hops:
            randomPeers.append(rps.getRandomPeer())
        onion.buildTunnel(destPeer, randomPeers)
        """

        #TODO: Respond the UI

    def _destryTunnel(self, onion, rawData):
        pass
        #tunnelId = socket.ntohl(rawData[:4])
        #onion.destroyTunnel(tunnelId)

    def _coverTraffic(self, onion, rawData):
        pass
        #onion.sendCoverTraffic(rps)

    def checkForData(self):
        readable, writable, exceptional = select.select([ self.connection ], [], [ self.connection ])

        if len(exceptional) > 0:
            raise Exception("UI Module connection failed")

        if len(readable) == 1:
            rawData = self.connection.recv(4)
            size = socket.ntohs(rawData[:2])
            id = socket.ntohs(int(str(rawData[2:4])))
            rawData = self.connection.recv(size - 4)

            print "rawData : " + rawData

            #TODO: Do threading here
            if id == UIConnectionType.ONION_TUNNEL_BUILD:
                print "build tunnel"
                #_buildTunnel(onion, rps, rawData)
            elif id == UIConnectionType.ONION_TUNNEL_DESTROY:
                print "tunnel destroy"
                #_destroyTunnel(onion, rawData)
            elif id == UIConnectionType.ONION_COVER:
                print "onion cover"
                #_coverTraffic(onion, rps, rawData)
            

