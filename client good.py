import socket
import select
import sys
import atexit
import datetime
import re

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
timestamps = True
maxlen = 16

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
                    if timestamps == True:
                        print(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%S")) + " " + message+"\a")
                    else:
                        print(message+"\a")
                else:
                    if timestamps == True:
                        print(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%X")) + " " + message)
                    else:
                        print(message)
        else:
            message = sys.stdin.readline()
            if message[:1] == "/":
                command = message.split(None,1)[0]
                try:
                    args = message.split(None, 1)[1]
                except:
                    args = None
                args = re.sub('[^a-zA-Z0-9_]', '', args)
                if command == "/iam":
                    try:
                    	if args.rstrip().lower() != "god":
                    		print "[me] You shall now be known as " + args.rstrip()[:maxlen]
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
                    print "[me] Some commands are available:\n/iam [username] - change your name\n/quit - leave the server\n/alerts - toggle the alerts\n/timestamps - toggle the timestamps\n/help - display this message\n/clear - clear the screen\n/becomegod - ASCEND"
                elif command == "/timestamps":
                    timestamps = not timestamps
                    print "[me] Most timestamps are now turned " + onoff(timestamps) 
                elif command == "/clear":
                    print '\033[2J'
                else:
                    print "[me] That command doesn't exist, try again genius\a"
                args = None
            else:
                sendmess(message)
                sys.stdout.write("\033[F")
                if timestamps == True:
                    sys.stdout.write(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%S")) + " ")
                if isgod == True:
                    sys.stdout.write("[you] ")
                else:
                    sys.stdout.write("<You> ")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()
