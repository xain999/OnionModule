# system imports
import socket
import struct
from threading import Thread

#user imports
from rpsConnection import *

class OnionAuthType(Enum):
    AUTH_SESSION_START          = 600
    AUTH_SESSION_HS1            = 601
    AUTH_SESSION_INCOMING_HS1   = 602
    AUTH_SESSION_HS2            = 603
    AUTH_SESSION_INCOMING_HS2   = 604
    AUTH_LAYER_ENCRYPT          = 605
    AUTH_LAYER_DECRYPT          = 606
    AUTH_LAYER_ENCRYPT_RESP     = 607
    AUTH_LAYER_DECRYPT_RESP     = 608
    AUTH_SESSION_CLOSE          = 609

class OnionAuthentication(object):
    def __init__(self, address, isIPv6):
        if address.ipv6:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.connect((address.ip, address.port))
        self.requestId = 0

    # starts authention and returns the response
    def authSessionStart(self, hopKey):
        # starting authentication session
        size = socket.htons(len(hopKey) + 4)
        packetType = socket.htons(OnionAuthType.AUTH_SESSION_START)
        packet = size + packetType + hopKey
        self.sock.sendall(packet)

        # receiving the response
        size = socket.ntohs(recv(self.sock, 2))
        packet = recvAll(self.sock, size - 2)
        packetType = socket.ntohs(packet[:2])
        sessionId = socket.ntohl(packet[2:6])

        if packetType != OnionAuthType.AUTH_SESSION_HS1:
            print ("OnionAuthentication Error! Exiting")
            exit(1)

        return sessionId, packet[6:]

    # msg on the hop and it's response
    def authSessionIncoming(self, hostKey, payload):
        size = socket.htons(len(payload) + len(hostKey) + 8)
        packetType = socket.htons(OnionAuthType.AUTH_SESSION_INCOMING_HS1)
        reserved = socket.htons(0)
        hostKeySize = socket.htons(len(hostKey))

        packet = size + packetType + reserved + hostKeySize + hostKey + payload
        self.sock.sendall(packet)

        # receiving the response
        size = socket.ntohs(recv(self.sock, 2))
        packet = recvAll(self.sock, size - 2)
        packetType = socket.ntohs(packet[:2])
        sessionId = socket.ntohl(packet[2:6])

        if packetType != OnionAuthType.AUTH_SESSION_HS2:
            print ("OnionAuthentication Error! Exiting")
            exit(1)

        return sessionId, packet[6:]

    
    def authSessionConfirm(self, sessionId, payload):
        # confirming authentication session
        size = socket.htons(len(payload) + 8)
        packetType = socket.htons(OnionAuthType.AUTH_SESSION_INCOMING_HS2)
        sessionIdPacket = socket.htonl(sessionId)
        packet = size + packetType + sessionIdPacket + payload
        self.sock.sendall(packet)

    
    def authLayerEncrypt(self, sessionIds, payload):
        # sending the encryption message
        size = sock.htons(len(payload) + len(sessionIds) * 4 + 8)
        packetType = socket.htons(OnionAuthType.AUTH_LAYER_ENCRYPT)
        sessionLen = struct.pack('>BB', len(sessionIds), 0)
        req = socket.htons(self.requestId)

        #making the packet
        packet = size + packetType + sessionLen + req

        for sess in sessionIds:
            packet += socket.htonl(sess)

        packet += payload
        self.sock.sendall(packet)

        # receiving the response
        size = socket.ntohs(recv(self.sock, 2))
        packet = recvAll(self.sock, size - 2)
        packetType = socket.ntohs(packet[:2])
        req = socket.ntohs(packet[2:4])

        if packetType != OnionAuthType.AUTH_LAYER_ENCRYPT_RESP:
            print ("OnionAuthentication Error! Exiting")
            exit(1)

        self.requestId = self.requestId + 1

        return packet[6:]

    def authLayerDecrypt(self, sessionIds, payload):
        # sending the decryption message
        size = sock.htons(len(payload) + len(sessionIds) * 4 + 8)
        packetType = socket.htons(OnionAuthType.AUTH_LAYER_DECRYPT)
        sessionLen = struct.pack('>BB', len(sessionIds), 0)
        req = socket.htons(self.requestId)

        #making the packet
        packet = size + packetType + sessionLen + req

        for sess in sessionIds:
            packet += socket.htonl(sess)

        packet += payload
        self.sock.sendall(packet)

        # receiving the response
        size = socket.ntohs(recv(self.sock, 2))
        packet = recvAll(self.sock, size - 2)
        packetType = socket.ntohs(packet[:2])
        req = socket.ntohs(packet[2:4])

        if packetType != OnionAuthType.AUTH_LAYER_DECRYPT_RESP:
            print ("OnionAuthentication Error! Exiting")
            exit(1)

        self.requestId = self.requestId + 1

        return packet[6:]

    def closeSession(self, sessionId):
        # sending the decryption message
        size = sock.htons(8)
        packetType = socket.htons(OnionAuthType.AUTH_SESSION_CLOSE)
        sessionIdPacket = socket.hton(sessionId)

        packet = size + packetType + sessionIdPacket
        self.sock.sendall(packet)