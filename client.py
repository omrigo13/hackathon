import socket
import struct

magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
team_name = "blabla"

print("Client started, listening for offer requests...")

#open a socket for broadcast message
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.bind(('', udp_port))
