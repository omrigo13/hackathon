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

while True:
 try:
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg, address = broadcast_socket.recvfrom(buffer_size)
    print("Received offer from " + address[0] + ", attempting to connect...")
    tcp_client_socket.connect((address[0], tcp_server_port))
    tcp_client_socket.send(team_name.encode())
    tcp_client_socket.close()

 except:
    tcp_client_socket.close()
    print("fail")