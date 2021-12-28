from random import randint
from socket import *
from scapy.arch import get_if_addr

tcp_server_port = 2040

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