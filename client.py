import socket
import struct
import sys
import time

from termcolor import colored

magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
timeout = 10
team_name = "noa without o"

print(colored("Client started, listening for offer requests...", "white"))

# open a socket for broadcast message
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.bind(('', udp_port))

while True:
    try:
        msg, address = broadcast_socket.recvfrom(buffer_size)
        print(colored("Received offer from " + address[0] + ", attempting to connect...", "green"))
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cookie, msg_type, tcp_server_port = struct.unpack('IBH', msg)
        if cookie != magic_cookie or msg_type != msg_type:
            print(colored("wrong broadcast message format", "red"))
            continue

        tcp_client_socket.connect((address[0], tcp_server_port))
        tcp_client_socket.send(team_name.encode())
        tcp_client_socket.settimeout(socket.getdefaulttimeout())
        msg_received = tcp_client_socket.recv(buffer_size)
        print(colored(msg_received.decode(), "magenta"))
        key = sys.stdin.readline()[0]
        tcp_client_socket.send(key.encode())
        end_msg = tcp_client_socket.recv(buffer_size)
        print(end_msg.decode())
        print(colored("Server disconnected, listening for offer requests...", "yellow"))
        time.sleep(5)
    except:
        tcp_client_socket.close()
