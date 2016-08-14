#from uiConnection import UIConnection
from onion import Onion
from rpsConnection import RPSConnection
from threading import Thread


def start_listening(config):
    #uiConn = UIConnection(config.apiAddress, config.apiAddress.ipv6, config.onionHops)

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
        o.checkForData(ui)