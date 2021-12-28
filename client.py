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
     cookie, type, tcp_server_port = struct.unpack('IBH', msg)
     if (cookie != magic_cookie or type != msg_type):
         print("wrong broadcast message format")
     continue
     tcp_client_socket.connect((address[0], tcp_server_port))
     tcp_client_socket.send(team_name.encode())
     msg_received = tcp_client_socket.recv(buffer_size)
     print(msg_received.decode())
     math_problem_answer(tcp_client_socket)
     tcp_client_socket.close()

 except:
    tcp_client_socket.close()
    print("fail")
