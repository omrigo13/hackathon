from random import randint
from socket import *
from scapy.arch import get_if_addr, struct
import time

tcp_server_port = 2040
magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
players = {}

def math_problem():
    num1 = randint(0,5)
    num2 = randint(0,4)
    return str(num1) + "+" + str(num2)

def tcp_socket():
    server_address = get_if_addr('eth1')
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((str(server_address), tcp_server_port))
    server_socket.listen()
    print("Server started, listening on IP address " + str(server_address))
    return server_socket

def udp_broadcast():
    udp_server_socket = socket(AF_INET, SOCK_DGRAM)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while len(players) < 2:
        msg = struct.pack('IBH', magic_cookie, msg_type, tcp_server_port)
        udp_server_socket.sendto(msg, ('<broadcast>', udp_port))
        time.sleep(1)