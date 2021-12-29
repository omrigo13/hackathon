import socket
import struct
import sys
import threading
import time
# import tty
import keyboard
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
        fd1, fd2 = tcp_client_socket.fileno(), sys.stdin.fileno()
        try:
            rlist, wlist, xlist = select.select([fd1, fd2], [], [], 10)
            if len(rlist) > 0:
                hd = rlist[0]
                if hd == fd2:
                    user_input = input('')
                    tcp_client_socket.send(user_input.encode())
        except:
            print('Call to select function failed')
        finally:
            summary = tcp_client_socket.recv(buffer_size)
            print(summary.decode())

        print ("Server disconnected, listening for offer requests...")
    except Exception as e:
        print(e)
        tcp_client_socket.close()
        # continue
        # print("fail")
