from random import randint
from socket import *
from scapy.arch import get_if_addr, struct
import time
from threading import Thread

from select import select

tcp_server_port = 2040
magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
timeout = 10
players = {}

def math_problem():
    num1 = randint(0,5)
    num2 = randint(0,4)
    return str(num1) + "+" + str(num2)

def tcp_socket():
    # server_address = get_if_addr('eth1')
    server_address = "192.168.0.112"
    # server_address = "192.168.0.103"
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((str(server_address), tcp_server_port))
    server_socket.listen()
    print("Server started, listening on IP address " + str(server_address))
    return server_socket

def udp_broadcast():
    udp_server_socket = socket(AF_INET, SOCK_DGRAM)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while len(players) < 1:
        msg = struct.pack('IBH', magic_cookie, msg_type, tcp_server_port)
        udp_server_socket.sendto(msg, ('<broadcast>', udp_port))
        time.sleep(1)

def listen_tcp(server_socket):
    global players
    while len(players) < 1:
        conn, addr = server_socket.accept()
        players[addr] = conn

def start_msg(team1_name, team2_name):
    player1 = "Player 1: " + team1_name + "\n"
    player2 = "Player 2: " + team2_name + "\n"
    question = math_problem()
    return "Welcome to Quick Maths.\n" + player1 + player2 + "==\nPlease answer the following question as fast as you can:\n" \
                                                             "How much is " + question + "?"

def end_msg(team1_name, team1_answer, team2_name, team2_answer, answer):
    correct_answer = "Game over!\nThe correct answer was " + answer + "!\n\n"
    winner_msg = "Congratulations to the winner: "
    if(team1_answer == answer) and team2_answer != answer:
        return correct_answer + winner_msg + team1_name
    elif (team1_answer != answer) and team2_answer == answer:
        return correct_answer + winner_msg + team2_name
    return "nobody answered, the game finished with a draw"

def game():
    global players
    team1_name = players.get(list(players.keys())[0]).recv(buffer_size).decode()
    print(team1_name)
    time.sleep(5)
    players.get(list(players.keys())[0]).send(start_msg(team1_name, "bb").encode())
    print("sent start message")
    reads,_,_  = select([list(players.keys())[0],list(players.keys())[0]],[],[], timeout)
    if len(reads) > 0:
        ans = players.get(list(players.keys())[0]).recv(buffer_size).decode()[:-1]
    print(ans)
server_socket = tcp_socket()
while True:
        broadcasts_thread = Thread(target=udp_broadcast)
        clients_thread = Thread(target=listen_tcp, args=(server_socket, ))
        broadcasts_thread.start()
        clients_thread.start()
        broadcasts_thread.join()
        clients_thread.join()
        time.sleep(10)
        game()
        time.sleep(10)
