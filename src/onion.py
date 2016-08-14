from onionAuthentication import OnionAuthentication, Peer
import socket
import select
import struct
from enum import Enum
import random
from address import Address


class OnionMsgType(Enum):
    TUNNEL_BUILD_HS1 = 663
    TUNNEL_BUILD_HS2 = 664
    TUNNEL_DATA = 665
    TUNNEL_ERROR = 666


class SocketStates(Enum):
    SENT_HS1 = 1


class Onion(object):
    def __init__(self, config):
        self.onion_auth = OnionAuthentication(config.onionAuthAddress)
        address = config.p2pAddress
        self.isIPv6 = True if address.ipv6 else False
        self.ip = address.ip

        if address.ipv6:
            self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((address.ip, address.port))
        self.server.listen(5)
        self.sockets = [self.server]

        self.sock_states = dict()

    def build_tunnel(self, destPeer, randomPeers):
        hop_chain = [peer for peer in randomPeers]
        hop_chain.append(destPeer)
        p = Peer("0.0.0.0", 0, False, "")
        hop_chain.append(p)

        for i in range(0, len(hop_chain)-1):
            self.build_hop(hop_chain[i], hop_chain[i+1])

    def build_hop(self, peer, next_peer):
        sessionId, hs1 = self.onion_auth.authSessionStart(peer.key)
        #print sessionId, hs1, peer.address.ip, peer.address.port
        tunnel_id = random.getrandbits(32)
        self.send_hs1(tunnel_id, peer.address, peer.key, hs1, next_peer.address)  # change peer.key to our key

    def send_hs1(self, tunnel_id, hop, host_key, hs1_payload, next_hop):
        msg = struct.pack("!HL", OnionMsgType.TUNNEL_BUILD_HS1, tunnel_id)
        if next_hop.ipv6:
            msg += socket.inet_pton(socket.AF_INET6, next_hop.ip)
        else:
            msg += socket.inet_pton(socket.AF_INET, next_hop.ip)
        msg += struct.pack("!HHHH", 0, next_hop.port, len(host_key), len(hs1_payload))
        msg += str.encode(host_key)
        msg += hs1_payload
        length = len(msg) + 2
        msg = struct.pack("!H", length) + msg

        if hop.ipv6:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hop.ip, hop.port))
        sock.sendall(msg)
        self.sockets.append(sock)
        self.sock_states[sock] = SocketStates.SENT_HS1

    def send_hs2(self, sock, tunnel_id, hs2_payload):
        msg = struct.pack("!HLHH", OnionMsgType.TUNNEL_BUILD_HS1, tunnel_id, 0, len(hs2_payload))
        msg += hs2_payload
        length = len(msg) + 2
        msg = struct.pack("!H", length) + msg
        sock.sendall(msg)



    def checkForData(self):
        readable, writable, exceptional = select.select(self.sockets, [], self.sockets)

        # Handle inputs
        for s in readable:
            if s is self.server:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                self.sockets.append(connection)
                self.handle_data(connection)
            else:
                self.handle_data(s)


    def handle_data(self, conn):
        rawData = conn.recv(4)

        if rawData:
            size = struct.unpack('!H', rawData[:2])[0]
            id = struct.unpack('!H', rawData[2:4])[0]
            rawData = conn.recv(size - 4)

            if id == OnionMsgType.TUNNEL_BUILD_HS1:
                self.handle_hs1(rawData)
            elif id == OnionMsgType.TUNNEL_BUILD_HS2:
                print "tunnel hs2"
            elif id == OnionMsgType.TUNNEL_DATA:
                print "tunnel data"
            elif id == OnionMsgType.TUNNEL_ERROR:
                print "tunnel error"

        else:
            self.sockets.remove(conn)
            conn.close()

    def handle_hs1(self, data):
        tunnel_id = int(struct.unpack("!L", data[0:4])[0])
        data = data[4:]

        if self.isIPv6:
            ip = socket.inet_ntop(socket.AF_INET6, data[0:16])
            data = data[20:]
        else:
            ip = socket.inet_ntop(socket.AF_INET, data[0:4])
            data = data[8:]

        nxt = struct.unpack("!HHHH", data[0:64])
        port = nxt[1]
        hostKeySize = nxt[2]
        hs1Size = nxt[3]
        data = data[64:]

        print tunnel_id, ip, port, hostKeySize, hs1Size, data

        if ip=="0.0.0.0":
            print "tunnel end here"
            return

