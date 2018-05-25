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

def onoff(boolean):
    if boolean:
        return "on"
    else:
        return "off"
def sendmess(messagetosend):
    server.send(messagetosend.rstrip())

atexit.register(exit_handler)

sockets_list = [sys.stdin, server]
read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
mynameis = raw_input("Who are you? ")
server.send("/iwasalways " + mynameis)
hastbegun = False
alertson = True
isgod = False

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if message == "[god] Wow, nice guess. Now you can type as me!":
                isgod = True
            if hastbegun == False:
                print(message)
                hastbegun = True
            else:
                if alertson == True:
                    print(message+"\a")
                else:
                    print(message)
        else:
            message = sys.stdin.readline()
            if message[:1] == "/":
                command = message.split(None,1)[0]
                try:
                    args = message.split(None,1)[1]
                except:
                    args = None
                if command == "/iam":
                    try:
                    	if args.rstrip() != "god":
                    		print "[me] You shall now be known as " + args.rstrip()
                        sendmess(message)
                        isgod = False
                    except:
                        print "[me] psst, you gotta pick a name, dude\a"
                elif command == "/quit":
                    print "oh no"
                    quit()
                elif command == "/becomegod":
                    if args:
                        sendmess(message)
                    else:
                        print "[me] I think you need a password...\a"
                elif command == "/alerts":
                    alertson = not alertson
                    print "[me] Most alerts are now turned " + onoff(alertson) 
                elif command == "/help":
                    print "[me] Some commands are available:\n/iam [username] - change your name\n/quit - leave the server\n/alerts - toggle the alerts\n/help - display this message\n/becomegod - ASCEND"
                else:
                    print "[me] That command doesn't exist, try again genius\a"
                args = None
            else:
                sendmess(message)
                sys.stdout.write("\033[F")
                if isgod == True:
                    sys.stdout.write("[you] ")
                else:
                     sys.stdout.write("<You> ")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()
