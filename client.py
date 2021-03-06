import socket
import struct
import sys
import time
from threading import Thread

from termcolor import colored

magic_cookie = 0xabcddcba;
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
timeout = 10
team_name = "noa with no h"
gameover =False
tcp_socket= None
def __listen_keyboard(): #thread waiting for keyboard
    key_press = sys.stdin.readline().replace('\n',"")
    if not gameover:
        tcp_socket.send(key_press.encode())


def __listen_gameover(): #thread waiting foe msg from server
    winner_message = tcp_socket.recv(buffer_size)
    gameover = True
    print(winner_message.decode())

print(colored("Client started, listening for offer requests...", "white"))

# open a socket for broadcast message
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.bind(('', udp_port))

while True:
    try:
        msg, address = broadcast_socket.recvfrom(buffer_size) # get the tcp port and ip of the server by the udp broadcast
        print(colored("Received offer from " + address[0] + ", attempting to connect...", "green"))
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cookie, msg_type, tcp_server_port = struct.unpack('IBH', msg)
        if cookie != magic_cookie or msg_type != msg_type:
            print(colored("wrong broadcast message format", "red"))
            continue

        tcp_client_socket.connect((address[0], tcp_server_port)) # make socket to connect to the server using tcp
        tcp_client_socket.send(team_name.encode()) # send team name
        msg_received = tcp_client_socket.recv(buffer_size) # receive math problem question

        print(colored(msg_received.decode(), "magenta"))

        try:
            tcp_socket = tcp_client_socket
            key_listen = Thread(target=__listen_keyboard )
            game_listen = Thread(target=__listen_gameover)
            key_listen.start()
            game_listen.start()

            game_listen.join()
        except :
            pass
            print(colored("threads", "red"))

        tcp_client_socket.close()
        gameover = False
        print(colored("Server disconnected, listening for offer requests...", "yellow"))
        time.sleep(1)
    except:
        tcp_client_socket.close()
        print(colored("server disconnected", "red"))
