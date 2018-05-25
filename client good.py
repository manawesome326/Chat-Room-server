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
    server.close()

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
            if message[:1] == "/":
                command = message.split()[0]
                try:
                    args = message.split()[1]
                except:
                    pass
                if command == "/iam":
                    try:
                        print "[you] You shall now be known as " + args
                        server.send(message)
                    except:
                        print "[you] psst, you gotta pick a name, dude"
                elif command == "/quit":
                    print "oh no"
                    quit()
                else:
                    print "[you] That command doesn't exist, try again genius"
                args = None
            else:
                server.send(message)
                sys.stdout.write("\033[F")
                sys.stdout.write("<You> ")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()
