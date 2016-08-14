#from uiConnection import UIConnection
from onion import Onion
from rpsConnection import RPSConnection
from threading import Thread
from uiConnection import UIConnection
from rpsConnection import RPSConnection

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
    rps = RPSConnection(config.rpsAddress, config.apiAddress.ipv6)
    uiConn = UIConnection(config.apiAddress, config.apiAddress.ipv6, config.onionHops, rps)

    #end = False
    #while not end:
    #    end = uiConn.checkForData()


    o = Onion(config)

    t = Thread(target=loop_listen, args=[o])
    t.start()

    rps = RPSConnection(config.rpsAddress, config.rpsAddress.ipv6)

    dest = rps.getRandomPeer()
    hops = [rps.getRandomPeer()]
    o.build_tunnel(dest, hops)

    t.join()

def loop_listen(o):
    while True:
        o.checkForData()