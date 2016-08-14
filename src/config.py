# system imports
import ConfigParser

#user imports
from address import *

class Config(object):
    def __init__(self, filename):
        # instatiating parser
        config = ConfigParser.ConfigParser()
        config.read(filename)
        
        # read values from a section
        self.maxRelayConnections = config.getint('ONION', 'max_relay_connections')
        self.onionHops = config.getint('ONION', 'onion_hops')
        p2pHostname = config.get('ONION', 'P2P_HOSTNAME')
        p2pPort = config.getint('ONION', 'P2P_PORT')
        self.p2pAddress = self._getAddress(p2pHostname, p2pPort)
        self.apiAddress = self._getAddress(config.get('ONION', 'api_address'))
        self.onionAuthAddress = self._getAddress(config.get('ONION_AUTHENTICATION', 'api_address'))
        self.rpsAddress = self._getAddress(config.get('RPS', 'api_address'))
        self.packetSize = int(config.get('ONION', 'packet_size'))
        #self.bool_val = config.getboolean('ONION', 'bool_val')
        #self.float_val = config.getfloat('ONION', 'pi_val')

    def _getAddress(self, address, port=None):
        if port is None:
            address, portStr = address.rsplit(':', 1)
            port = int(portStr)
        if ':' in address:
            if '[' in address:
                address = address[1:-1]
            return Address(address, port, True)
        return Address(address, port, False)

    @staticmethod
    def readConfiguration(filename):
        return Config(filename)