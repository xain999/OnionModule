import socket


def create_socket(address, is_listen=False):
    if address.ipv6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        addr = '' if is_listen else address.ipv6
        sock.bind((addr, address.port))
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = '' if is_listen else address.ip
        sock.bind((addr, address.port))

    return sock

def recv_all(sock, size):
    data = ''

    while size > 0:
        recvd = sock.recv(size)
        size -= len(recvd)
        data = data + recvd

    return data