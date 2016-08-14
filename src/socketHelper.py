import socket


def create_socket(address):
    if address.ipv6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.bind((address.ipv6, address.port))
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address.ip, address.port))

    return sock

def recv_all(sock, size):
    data = ''

    while size > 0:
        recvd = sock.recv(size)
        size -= len(recvd)
        data = data + recvd

    return data