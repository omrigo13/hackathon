import socket
import struct
import msvcrt
import sys
import threading
import time
import tty
import keyboard
from msvcrt import getch

from select import select

magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
timeout = 10
team_name = "blabla"




print("Client started, listening for offer requests...")

# open a socket for broadcast message
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.bind(('', udp_port))

while True:
    try:
        msg, address = broadcast_socket.recvfrom(buffer_size)
        print("Received offer from " + address[0] + ", attempting to connect...")
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.settimeout(10)
        cookie, msg_type, tcp_server_port = struct.unpack('IBH', msg)
        if cookie != magic_cookie or msg_type != msg_type:
            print("wrong broadcast message format")
            continue
        tcp_client_socket.connect((address[0], tcp_server_port))
        tcp_client_socket.send(team_name.encode())
        print("sent name")
        tcp_client_socket.settimeout(socket.getdefaulttimeout())
        msg_received = tcp_client_socket.recv(buffer_size)
        print(msg_received.decode())
        print("i got here1")
        # reads, _, _ = select([sys.stdin, tcp_client_socket], [], [], timeout)
        # print("i got here2")
        # if len(reads) > 0 and reads[0] == sys.stdin:
        #     question_answer = sys.stdin.readline()
        # question_answer = getch()
        # print(question_answer)
        # tcp_client_socket.send(question_answer.encode())
        # print("sent answer")
        # answer = tcp_client_socket.recv(buffer_size)
        # print(answer.decode())
        # tcp_client_socket.close()
        #  Windows
        # key = keyboard.read_key()  # in my python interpreter, this captures "enter up"
        reads,_,_ = select([sys.stdin, tcp_client_socket],[],[],10)
        if len(reads) > 0 and reads[0] == sys.stdin:
            ans = sys.stdin.readline()[0]
        # now = time.time()
        # if time.time()<now+10:
        #     key = sys.stdin.readline()[0]
        #     tcp_client_socket.send(key.encode())
        #     print("sent key")

        # answer = msvcrt.getch()
        # answer = answer.decode('utf-8')
        #
        # tcp_client_socket.send(answer.encode())
        #
        data = tcp_client_socket.recv(buffer_size).decode()  # receive response
        print(data)

    except Exception as e:
        print(e)
        tcp_client_socket.close()
        # continue
        # print("fail")
