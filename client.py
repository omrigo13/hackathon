import socket
import struct
import sys
import threading
import time
import tty
import keyboard
import termios
import select

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
        if address[0] == "172.18.0.40":
            print("Received offer from " + address[0] + ", attempting to connect...")
            tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            
            # reads,_,_ = select([sys.stdin, tcp_client_socket],[],[],10)
            # if len(reads) > 0 and reads[0] == sys.stdin:
            #     ans = sys.stdin.readline()[0]
            #     tcp_client_socket.send(ans.encode())
            # else: 
            #     ans = ""
            #     tcp_client_socket.send(ans.encode())
        
            # data = tcp_client_socket.recv(buffer_size).decode()  # receive response
            # print(data)
            # read_sockets = [sys.stdin, tcp_client_socket]
            # old_info_stdin = termios.tcgetattr(sys.stdin)
            # tty.setcbreak(sys.stdin.fileno())
            # readable_sockets = select.select.select(read_sockets, [], [])[0]
            # if readable_sockets[0] is sys.stdin: # If we need to read input from the keyboard
            #     # TODO: check if need to support messages before server welcom message

            #     user_answer = sys.stdin.read(1) # Read one digit in a non blocking way
            #     print( user_answer) # Print the digit to the screen

            #     # if (user_answer.isdigit()): # If the input is really a digit
            #     #     digit_value = ord(user_answer) - ord('0')
            #     #     clientSocket.send(digit_value.to_bytes(1, ENDIAN)) # Send the input to the answer as it's value and not in ascii
            #     tcp_client_socket.send(user_answer.encode())
            # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_info_stdin)
            flag = True
            while flag:
        

       # char = getch.getch():
        
        
                try:
                    keyboard.on_press_key(x, lambda _:clientSocket.send(x))
                    flag = False
            #clientSocket.send(char)
                except:
                    flag = False
                break

            game_results_message = tcp_client_socket.recv(buffer_size) # Get the game result from the server
            print(game_results_message.decode())
            print ("Server disconnected, listening for offer requests...")
    except Exception as e:
        print(e)
        tcp_client_socket.close()
        # continue
        # print("fail")
