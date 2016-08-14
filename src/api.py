from uiConnection import UIConnection
from onion import Onion
from rpsConnection import RPSConnection
from threading import Thread


def start_listening(config):
    print "Connecting to RPS server"
    rps = RPSConnection(config.rpsAddress, config.rpsAddress.ipv6)
    print "Connecting to UI server"
    uiConn = UIConnection(config.apiAddress, config.apiAddress.ipv6, config.onionHops, rps)

    o = Onion(config)

    print "Starting thread to listen on UI and Onion sockets"
    t = Thread(target=loop_listen, args=[o, uiConn])

    print "Listening to requests"
    t.start()

    t.join()


def loop_listen(o, ui):
    while True:
        ui.checkForData(o)
        o.checkForData(ui)
