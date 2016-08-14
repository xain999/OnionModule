import socket
import struct
from socketHelper import create_socket
from threading import Thread
from uiConnection import UIConnection

""""
def _parse_request(rawData):
    try:
        size = struct.unpack('!H', rawData[:2])[0]
        id = struct.unpack('!H', rawData[2:4])[0]
        rawData = rawData[4:size]
    except TypeError:
        print "Invalid packet"
        # TODO: Handle this better, send a tunnel error response
        return

    print (size, id, rawData)

    if id == UIConnectionType.ONION_TUNNEL_BUILD:
        print UIConnectionType.ONION_TUNNEL_BUILD
        #_buildTunnel(rawData)
    elif id == UIConnectionType.ONION_TUNNEL_DESTROY:
        print UIConnectionType.ONION_TUNNEL_DESTROY
        #_destroyTunnel(rawData)
    elif id == UIConnectionType.ONION_COVER:
        print UIConnectionType.ONION_COVER
        #_coverTraffic(rawData)
    else:
        print "Unknown packet type"


def _handle_api_request(conn, addr):
    data = ""
    while 1:
        recvd = conn.recv(1024)
        data += recvd
        if not recvd:
            break
    print "Received: %s " % data

    _parse_request(data)

    conn.close()
"""


def start_listening(config):
    uiConn = UIConnection(config.apiAddress, config.apiAddress.ipv6, config.onionHops)
    while True:
        uiConn.checkForData()
