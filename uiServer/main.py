import socket
import select
import struct

ONION_TUNNEL_BUILD = 560
ONION_TUNNEL_READY = 561
ONION_TUNNEL_INCOMING = 562
ONION_TUNNEL_DESTROY = 563
ONION_TUNNEL_DATA = 564
ONION_ERROR = 565
ONION_COVER = 566

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 30030)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

connected = False
tunnelId = None
port = 32032
ip = '127.0.0.1'

# Receive the data in small chunks and retransmit it
while True:

    print("Select:")
    print("\t1. Build Tunnel")
    print("\t2. Check for Data")
    print("\t3. Send Data")
    print("\t4. Tunnel Destroy")
    print("\t5. Send Cover Traffic")

    user = int(input("Enter a number: "))

    if user == 1:

        #msg = struct.pack(">hhh", ONION_TUNNEL_BUILD, 0, port)

        msg = socket.htons(ONION_TUNNEL_BUILD)
        msg += socket.htons(0)
        msg += socket.htons(port)
        msg += socket.inet_pton(socket.AF_INET, ip)
        msg += str.encode('-----BEGIN PUBLIC KEY-----')
        msg += str.encode('MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAs+kBcVXsFV6mKuXh9OKZ')
        msg += str.encode('VdkP0MoUl90eE4YS/jT5XMtcUPkVdoPDcmozujPe39dnfP/f6ZgzbPcZQ/6oCHWC')
        msg += str.encode('2LRJb/3HfwZ+00rwB4IzOy/6NfyVkcbRHqrGLJDyTooi5PedPv/JqKy08E1lqrsj')
        msg += str.encode('zYRGp+vo4I7eCNE+9qMerElay2laoom4ZVgDYLyvfep7CIQMOakbZQTdPrRqFD13')
        msg += str.encode('QJZhh0iRNNkYn4WrDSqN9X+2ZHzqbOu66mtMAl/OFIrCTOEpqTdVcxE3o+8dyb4g')
        msg += str.encode('0q5l04nscPCg7sygPmF13HetfrwDt+LhX3uSi+cs4vyH2GNsQ8OBgxDCEAFhMyQv')
        msg += str.encode('wMjUJHcAl2Wmw0nBgCA0xA3D1aEQT9IM5aY2GnBpfVLCeMjQf5NNMlVAoj6Fpy28')
        msg += str.encode('9sq9PmMw6NzpbNvmHl0nrlsbOoAZcs3m/c8ldB/YLPs+ADMncBsOLTqN7T33R7zA')
        msg += str.encode('ENjWNwnwPmZ04OXD/9dlPkQ1sel5x6l615h0Z7uN3K168q1bQZOug+UhQwI8dJNd')
        msg += str.encode('gd0MNcgKEp8ATYXK+V8vz/8I0CN0ywblnIyG9d+nMp6zsmo/58b6cngCoab2WsqU')
        msg += str.encode('n589nQCQqUsWMBLSFnaRNEwwX7ipqbFkDTwGkLEAjt4e9iGGBBk9U+iWGPN5RSMa')
        msg += str.encode('Y1CVSkwZ2LDUqsWB/gACpQ8CAwEAAQ==')
        msg += str.encode('-----END PUBLIC KEY-----')
        length = len(msg)
        msg = str(socket.htons(length)) + msg
        sock.send(msg)

    elif user == 2:
        readable, writable, exceptional = select.select([sock], [], [sock])

        if len(readable) > 0:
            print("SOCKET HAS DATA!")

            size = socket.ntohs(sock.recv(2))
            packet = sock.recv(size - 2)
            packetType = packet[:2]

            if packetType == ONION_TUNNEL_READY:
                tunnelId = packet[2:6]
                key = packet[6:]

                print("TUNNEL READY")
                print("size: " + str(size))
                print("packetType: " + str(packetType))
                print("tunnelId: " + str(tunnelId))
                print("key: " + key)
                print("\n")

                connected = True

            elif packetType == ONION_TUNNEL_INCOMING:
                tunnelId = packet[2:6]
                key = packet[6:]

                print("INCOMING TUNNEL")
                print("size: " + str(size))
                print("packetType: " + str(packetType))
                print("tunnelId: " + str(tunnelId))
                print("key: " + key)
                print("\n")

            elif packetType == ONION_TUNNEL_DESTROY:
                tunnelId = packet[2:6]

                print("TUNNLE DESTROY MESSAGE RECEIVED!")
                print("size: " + str(size))
                print("packetType: " + str(packetType))
                print("tunnelId: " + str(tunnelId))

                print("\n")

        else:
            print("NO DATA AVAILABLE!")

    elif user == 3:
        if not connected:
            print("NO TUNNEL CONNECTED")
            continue

        msg = struct.pack(">hI", ONION_TUNNEL_DATA, tunnelId)
        msg += str.encode('Ill take you to the candy shop')
        msg += str.encode('I ll let you lick the lollipop')
        msg += str.encode('Go  head girl dont you stop')
        msg += str.encode('Keep going til you hit the spot, whoa')
        msg += str.encode('I ll take you to the candy shop (yeah)')
        msg += str.encode('Boy, one taste of what I got (uh-huh)')
        msg += str.encode('I ll have you spending all you got (come on)')
        msg += str.encode('Keep going til you hit the spot, whoa')

        length = len(msg)
        msg += socket.htons(length)
        sock.sendall(msg)

    elif user == 4:
        if not connected:
            print("NO TUNNEL CONNECTED")
            continue

        msg = struct.pack(">hhI", 8, ONION_TUNNEL_DESTROY, tunnelId)
        sock.sendall(msg)
        connected = False
        tunnelId = 0

    elif user == 5:
        print("AT THE MOMENT DOES NOTHING")


