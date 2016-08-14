# system imports
import socket
import struct
from threading import Thread


def recv_all(sock, size):
    data = bytearray()

    while size > 0:
        recvd = sock.recv(size)
        size -= len(recvd)
        data += data + recvd

    return data


class OnionAuthType(enumerate):
    AUTH_SESSION_START = 600
    AUTH_SESSION_HS1 = 601
    AUTH_SESSION_INCOMING_HS1 = 602
    AUTH_SESSION_HS2 = 603
    AUTH_SESSION_INCOMING_HS2 = 604
    AUTH_LAYER_ENCRYPT = 605
    AUTH_LAYER_DECRYPT = 606
    AUTH_LAYER_ENCRYPT_RESP = 607
    AUTH_LAYER_DECRYPT_RESP = 608
    AUTH_SESSION_CLOSE = 609


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 20020)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

idGenerator = 100
openConnections = []

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    print('connection from', client_address)

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(4)

        if data:
            size = struct.unpack('!H', data[:2])[0]
            print("size: " + str(size[0]))
            id = struct.unpack('!H', data[2:4])[0]
            print("id: " + str(id[0]))

            data = recv_all(connection, size - 4)

            if id == OnionAuthType.AUTH_SESSION_START:
                packet = struct.pack('!HL', OnionAuthType.AUTH_SESSION_HS1, idGenerator)
                openConnections.append(idGenerator)
                idGenerator += 1
                packet += "Ya HS1 ha!"
                packet = struct.pack('!H', len(packet) + 2) + packet
                connection.sendall(packet)

            elif id == OnionAuthType.AUTH_SESSION_INCOMING_HS1:
                hostKeySize = struct.unpack('!H', data[2:4])[0]
                hostKey = data[4:hostKeySize + 4]
                data = data[hostKeySize + 4:]
                print("Data received: " + str(data))

                packet = struct.pack('!HL', OnionAuthType.AUTH_SESSION_HS2, idGenerator)
                openConnections.append(idGenerator)
                idGenerator += 1
                packet += "Ya HS2 ha!"
                packet = struct.pack('!H', len(packet) + 2) + packet
                connection.sendall(packet)

            elif id == OnionAuthType.AUTH_SESSION_INCOMING_HS2:
                print("Data received: " + str(data))

            elif id == OnionAuthType.AUTH_LAYER_ENCRYPT:
                layers = int(data[:1])
                reqId = struct.unpack('!H', data[2:4])[0]
                payloadStart = 4 + layers * 4

                data = data[payloadStart:]

                packet = struct.pack('!HHH', OnionAuthType.AUTH_LAYER_ENCRYPT_RESP, reqId, 0)
                packet += data
                packet = struct.pack('!H', len(packet) + 2) + packet
                connection.sendall(packet)

            elif id == OnionAuthType.AUTH_LAYER_DECRYPT:
                layers = int(data[:1])
                reqId = struct.unpack('!H', data[2:4])[0]
                payloadStart = 4 + layers * 4

                data = data[payloadStart:]

                packet = struct.pack('!HHH', OnionAuthType.AUTH_LAYER_DECRYPT_RESP, reqId, 0)
                packet += data
                packet = struct.pack('!H', len(packet) + 2) + packet
                connection.sendall(packet)

            elif id == OnionAuthType.AUTH_SESSION_CLOSE:
                sessId = struct.unpack('!H', data[:4])[0]
                openConnections.remove(sessId)

            else:
                print("FUCK YOU! THIS IS WRONG ID")

        else:
            connection.close()
            break

