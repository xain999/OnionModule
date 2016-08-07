# system imports
import sys

# user imports
from config import *
from rpsConnection import *


def main():
    print(sys.version)
    config = Config.readConfiguration("../config.ini")
    print(config)
    print("abc")

    #socket connect to the UI module

    #connect to RPS module
    rps = RPSConnection(config.rpsAddress, config.apiAddress.ipv6)
    print('done')
    peer = rps.getRandomPeer()

    #open tcp socket for p2p on new thread
    #whenever a new connection arrives, open special UDP socket and add both of them to global open sockets lists

    #while True:
        #check for data on p2p tcp list
        #if data, take approriate actions

        #check for data on p2p udp socket list
        #if data, relay or pass to UI module if connected

        #UI module not connected, check for new connections
        #if connected check for data
        #if data take appropriate actions 


if __name__ == "__main__":
    main()