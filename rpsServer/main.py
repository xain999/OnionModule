import socket
import sys
import struct

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10010)
print('starting up on %s port %s' % server_address)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()

    print ('connection from', client_address)

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(4)

        if data:
            size = struct.unpack("!H", data[:2])[0]
            print("size: " + str(size))
            id = struct.unpack("!H", data[2:4])[0]
            print("id: " + str(id))

            if id == 540:
                msg = struct.pack("!HHH", 541, 10010, 0)
                msg += socket.inet_aton('127.0.0.1')
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
                length = len(msg) + 2
                msg = str(struct.pack("!H", length)) + msg
                connection.send(msg)

        else:
            connection.close()
            break


# private key

# -----BEGIN RSA PRIVATE KEY-----
# MIIJKgIBAAKCAgEAs+kBcVXsFV6mKuXh9OKZVdkP0MoUl90eE4YS/jT5XMtcUPkV
# doPDcmozujPe39dnfP/f6ZgzbPcZQ/6oCHWC2LRJb/3HfwZ+00rwB4IzOy/6NfyV
# kcbRHqrGLJDyTooi5PedPv/JqKy08E1lqrsjzYRGp+vo4I7eCNE+9qMerElay2la
# oom4ZVgDYLyvfep7CIQMOakbZQTdPrRqFD13QJZhh0iRNNkYn4WrDSqN9X+2ZHzq
# bOu66mtMAl/OFIrCTOEpqTdVcxE3o+8dyb4g0q5l04nscPCg7sygPmF13HetfrwD
# t+LhX3uSi+cs4vyH2GNsQ8OBgxDCEAFhMyQvwMjUJHcAl2Wmw0nBgCA0xA3D1aEQ
# T9IM5aY2GnBpfVLCeMjQf5NNMlVAoj6Fpy289sq9PmMw6NzpbNvmHl0nrlsbOoAZ
# cs3m/c8ldB/YLPs+ADMncBsOLTqN7T33R7zAENjWNwnwPmZ04OXD/9dlPkQ1sel5
# x6l615h0Z7uN3K168q1bQZOug+UhQwI8dJNdgd0MNcgKEp8ATYXK+V8vz/8I0CN0
# ywblnIyG9d+nMp6zsmo/58b6cngCoab2WsqUn589nQCQqUsWMBLSFnaRNEwwX7ip
# qbFkDTwGkLEAjt4e9iGGBBk9U+iWGPN5RSMaY1CVSkwZ2LDUqsWB/gACpQ8CAwEA
# AQKCAgBJet5C+vPsmnbFyJRsH2y/GmOSRCb7C62wDa+OMfazBsAStlkkyZY3EddE
# stDRnbm/3QYH80j1tUqVcdoRcmVZuvDPk9g6Ml30UIQOnQftoZ/REvPH0Wsx2lAM
# fbrphxPPbq7Dv1cO1FMmXoYqoDp0QxVUmk7IALIA6e2McH0jouY5dDM3dYZhpfvj
# M819YRqVFNGlb0MoFD+Ez80PrTcaoxD8XxAnhI/A/6goPXwzi9Dj4/0fNXxnKCGo
# Spbx3uaS3dfVLCtzTtHp28zPzB69zcr7BjcSvcUNI3hDYizwOdUbkRD3tuuTwvXM
# vEOiBcA6Cgl698vayypnvRiE+b+ijKuOJ5O0SatSmGXFVkAq23qMGFCBfa6/iUY2
# 6UzE9vItAGDvzSHbL/Ubve5L13qVJnC9odzoSq8DIfdjB3RCMOe75YRdouqmljk1
# 6BP5ZIRPIGzGxyMZ/9IjVkqlqLCkPhhsfVSpmzyP0auB2GCtk3qQ/D6Hs5E6cgK2
# yqiOuUmc9vHjMoebnY7EdCVn7EIvfH2PEpVKFbvrKuP7T6LMz8r5Qev4yqqrfqfz
# VtmrklqyE/Hfvx5zsOII63bLDzkaTm+cQs4mYPFH5wJnwinAI6SdLqc3AHTAinT7
# VBKd1d+ru4uJBXJeLQxUor2xADV62TXNj28ruTesDvPCTp76cQKCAQEA/2vKw564
# dNg0fa5Hc9SvSl5udTj1X36LvW4QPZx4sdLKoMD+Begi/m7+ws3kIZv6nzrB/pbK
# N3al+mir8mPf4cxlyxFje7MChwjbuPBukwjeSUJ707p40ezLcZxxTYiSw8TbmAnf
# 5sqWJkxEcPFDEj8enzcIw8pIhCvkRFNemZCbSdBxUZJATGOh4p6HyWFd0FR8+Ke8
# XWXujZRI3g1wi5F37PAnLc0dbxvSZ+4GcP2QLJaliXqTDYdUNWyybW+CQ/n2Tuvb
# s7smjBL4k5sr13gwNiM13K/Ygan2r78cnj9Vto5LstYg1D+I05wkVsHs2hD/Avb3
# kL5tpptriU9g5wKCAQEAtFFl/690mERWDAax727xSzESouD3jcNt7TPOLeg5pQwk
# sAXwuUmM/jIm5uumG9uLVV9Y1ndOIrIfAP0qM2B81XeuQeW5O5JkiO3RBKe/F0oN
# aTOu6WF8M6S6AWWiyRi04vmEoUJp8C8qEMI7FLbG2Y1UF8bkaAdcngDo3pLq79il
# QPNbPQ/99Z9viO/qpl4UKr0Z37m+4ujflCdKGy5JC+PUJ274gKmSUPvBjZ2CaFEz
# WEJX5KrCc/Ft90ieC0tp2pmxIkQDdHNBOXJ9+IXm0MaGEjr1GevKxCjrcSVFhgLd
# Pi+2UyWkTcjJ/uJJHIt3k0nl/a3Bx8TbHL2u+GoNmQKCAQEArw29Zdy+JraXIxvy
# tJwrlxipM4XaBZzBQQ7R6qf2wEjrvskGUB4M/bwstm5N0AsK9V5b3pSR+vlCQCDE
# 19dDdYmUqlw8hmblcI7NqC6AWh1V23fJTg8bByT3OeIydSUJEUs2BTmfTpnB1nWm
# 4pE3mqXP4ubhBu74TD2YsItC5pSJGUnWoEVP9ArExIBKJ+anWUTOcczj+E8H89iR
# KD6lx8HnI2hkMavGZIP47Gnh2EawLR8CTPrJFhiNyh+5Ge+2o8gI24YiiUfW32GR
# I/jRT1d8E16GZ73M8PD/tOuSPZLCt99GWkcPMOhqaj01WpCGN942KF4Cxhz9IZab
# WPwiOQKCAQEAn7GLLON91jCHKEVxpoRRrG78e0XT2DghDbcYvW1yR+q2PzIznFU4
# ShOugkpmpTtNbcFwkxe8Glw3uw97JV8pj4Bb0r6Zytl+sgo0V/Qb94s8z1PXb5dH
# gRE9LmmNvp1j7bRfstV3ryCGF6t82X56I0fYFuqtdDg43TIfCqeA7AOpbxlXT3/v
# QW3/QH6CCO8+2w74cDw3gwwMnlAhgGsAhEg0puvPp1sGWzRrmXjKeoqXd23iG4Dj
# j/1cj2k/lu8mA1SkHJ2xlZtRQ4hTahtkbLe1G0YdteQugoVe5qjEpse4mw90YLTw
# i3bs9hAAAgi+ULJcvsr42GxORWj0IcsC2QKCAQEA6Dr7+v3O9hpBvko7Sr5Ar74o
# yOjJS/37yMc1XyHF7j7BrTw2OX3c+Uiz3ISK1e6Z727yoX+aHpLiAuJloruPvojf
# v6u4K22AozwazK6pjxsZUgZjlUitctDY3Jq+BNE6DB29AmDnMaVMhMalBtpiI4DK
# JIFmPVV2i91Zj2dBRbVeq+KCgZRFGJIUOhWQNRk8TmuarsIsgacuztLrwPkA80J5
# 7umVATC0sxEGnpkgUSNZqlD9FtIhswR/RXHs0aQtffji85nxuSFHc1Sy0vaF0ptA
# a5YkBJQMYBXewfkGOLc9IafrLLfiUUStzr9OOxILWCyMg205sZPUQDQFSpCVew==
# -----END RSA PRIVATE KEY-----














