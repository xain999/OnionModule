"""
Module to test api connections, very hacky
"""
import socket


def send_message(m):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 30030))
    sock.sendall(m)
    sock.close()


if __name__ == "__main__":
    send_message("hello world")

