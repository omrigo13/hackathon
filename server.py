import math
from random import randint
from socket import *
from scapy.arch import get_if_addr, struct
import time
from threading import Thread
import sys
from select import select
from termcolor import colored

tcp_server_port = 2040
magic_cookie = 0xabcddcba
msg_type = 0x2
udp_port = 13117
buffer_size = 1024
timeout = 10
players = {}
first_answered = 0
fastest_team = [0,math.inf]

# print(sys.argv)

def math_problem():
    num1 = randint(0,5)
    num2 = randint(0,4)
    return str(num1) + "+" + str(num2), num1 + num2

def tcp_socket():
    # server_address = get_if_addr('eth1')
    # server_address = "172.18.0.40"
    server_address = gethostbyname(gethostname())
    # server_address = "192.168.0.111"
    # server_address = "192.168.0.103"
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((str(server_address), tcp_server_port))
    server_socket.listen()
    print(colored("Server started, listening on IP address " + str(server_address), "blue"))
    return server_socket

def udp_broadcast(): # make udp connection for sending broadcast messages and let clients connect to the server
    udp_server_socket = socket(AF_INET, SOCK_DGRAM)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udp_server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    while len(players) < 2: # still send broadcast messages until you found two clients to start a game with
        msg = struct.pack('IBH', magic_cookie, msg_type, tcp_server_port)
        udp_server_socket.sendto(msg, ('<broadcast>', udp_port))
        time.sleep(1)


def listen_tcp(server_socket):
    global players
    while len(players) < 2: # accept players to the game and update the connection between them to the server
        conn, addr = server_socket.accept()
        players[addr] = conn


def fastest_team_msg():
    return "the fastest team so far is team: " + fastest_team[0] +" with time of "+str(fastest_team[1])


def start_msg(team1_name, team2_name):
    player1 = "Player 1: " + team1_name + "\n"
    player2 = "Player 2: " + team2_name + "\n"
    question, answer = math_problem()
    return "Welcome to Quick Maths.\n" + player1 + player2 + "==\nPlease answer the following question as fast as you can:\n" \
                                                             "How much is " + question + "?", str(answer)


def end_msg(team1_name, team1_answer, team2_name, team2_answer, answer, answered_first, times):
    global fastest_team
    correct_answer = "Game over!\nThe correct answer was " + answer + "!\n\n"
    winner_msg = "Congratulations to the winner: "
    if(team1_answer == answer) and team2_answer != answer and answered_first == 1:
        try :
            team1_answer_int = int(team1_answer)
            if 9 >= team1_answer_int >= 0:
                if times < fastest_team[1]:
                    fastest_team[0] = team1_name
                    fastest_team[1] = times
                return correct_answer + winner_msg + team1_name +'\n'+fastest_team_msg()+'\n'
        except:
            return correct_answer + winner_msg + team2_name+'\n'+fastest_team_msg()+'\n'

    elif (team1_answer != answer) and team2_answer == answer and answered_first == 2:
        try :
            team2_answer_int = int(team2_answer)
            if 9 >= team2_answer_int >= 0:
                if times < fastest_team[1]:
                    fastest_team[0] = team2_name
                    fastest_team[1] = times
                return correct_answer + winner_msg + team2_name+'\n'+fastest_team_msg()+'\n'
        except:
            return correct_answer + winner_msg + team1_name+'\n'+fastest_team_msg()+'\n'

    elif team1_answer != answer and answered_first == 1:
        return correct_answer + winner_msg + team2_name+'\n'+fastest_team_msg()+'\n'
    elif team2_answer != answer and answered_first == 2:
        return correct_answer + winner_msg + team1_name+'\n'+fastest_team_msg()+'\n'
    return "nobody answered, the game finished with a draw"

def game():
    try:
        global players
        global first_answered
        team1_socket = players.get(list(players.keys())[0])
        team2_socket = players.get(list(players.keys())[1])
        team1_name = team1_socket.recv(buffer_size).decode()
        team2_name = team2_socket.recv(buffer_size).decode()
        print(team1_name)
        print(team2_name)
        time.sleep(10)
        start, math_answer = start_msg(team1_name, team2_name)
        team1_socket.send(start.encode())
        team2_socket.send(start.encode())
        print("sent start message")
        times=time.time()
        reads,_,_  = select([team1_socket, team2_socket],[],[], timeout)
        ans1 = ""
        ans2 = ""
        if len(reads) > 0:
            if reads[0] == team1_socket:
                ans1 = team1_socket.recv(buffer_size).decode()
                times = time.time()-times
                first_answered = 1
            elif reads[0] == team2_socket:
                ans2 = team2_socket.recv(buffer_size).decode()
                times = time.time() - times
                first_answered = 2


        end = end_msg(team1_name, ans1, team2_name, ans2, math_answer, first_answered, times)
        team1_socket.send(end.encode())
        team2_socket.send(end.encode())
        team1_socket.close()
        team2_socket.close()
        players = {}
        first_answered = 0
    except :
        team1_socket.close()
        team2_socket.close()
        players = {}
        first_answered = 0
        print(colored("teams are disconnected", "red"))
        print(colored("Server started, listening on IP address " + str(server_address), "blue"))


server_socket = tcp_socket()
while True:
        broadcasts_thread = Thread(target=udp_broadcast)
        clients_thread = Thread(target=listen_tcp, args=(server_socket, ))
        broadcasts_thread.start()
        clients_thread.start()
        broadcasts_thread.join()
        clients_thread.join()
        # time.sleep(10)
        game()
        time.sleep(10)
