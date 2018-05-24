import socket
import select
import sys
import atexit

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

def exit_handler():
    server.send("/quit")

atexit.register(exit_handler)

sockets_list = [sys.stdin, server]
read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
mynameis = raw_input("Who are you? ")
server.send("/iwasalways " + mynameis)
hastbegun = False
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if hastbegun == False:
                print(message)
                hastbegun = True
            else:
                print(message+"\a")
        else:
            message = sys.stdin.readline()
            if message[:1] == "/": # Checks if the user entered a command
                command = message.split()[0]
                if len(message.split()) > 1:
                    args = message.split()[1]
                if command == "/iam":
                    print "You shall now be known as " + args
                if command == "/quit":
                    print "oh no"
                    quit()
                server.send(message)
            else:
                server.send(message[:-1])
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()