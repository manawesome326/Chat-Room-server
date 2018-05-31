import socket
import select
import sys
import atexit
import datetime
import re

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number" #ya numpty
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

def exit_handler():
    server.send("/quit") #quits when you quit
    server.close()

def onoff(boolean):
    if boolean:
        return "on"
    else:
        return "off" 
    #don't change this
def sendmess(messagetosend):
    server.send(messagetosend.rstrip())
    #gets rid of weirdo whitespace before sending messages

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
        if socks == server: # idk what this means
            message = socks.recv(2048)
            if message == "[god] Wow, nice guess. Now you can type as me!": #just checks if we're god now
                isgod = True 
            if hastbegun == False: #never bongs on the first message
                print(message)
                hastbegun = True
            else:
                if alertson == True:
                    if timestamps == True:
                        print(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%S")) + " " + message+"\a")
                    else:
                        print(message+"\a") #prints message. Bong!
                else:
                    if timestamps == True:
                        print(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%X")) + " " + message)
                    else:
                        print(message) #prints message
        else:
            message = sys.stdin.readline()
            if message[:1] == "/": #checks for commands
                command = message.split(None,1)[0]
                try:
                    args = message.split(None, 1)[1]
                    args = re.sub('[^a-zA-Z0-9_\\ ]', '', args) #gets rid of weirdo characters in args
                except:
                    args = None
                if command == "/iam": #urgh this stuff sucks
                    try:
                        if args.rstrip().lower() != "god":
                            print "[me] You shall now be known as " + args.rstrip()[:maxlen]
                        sendmess(message)
                        isgod = False
                    except:
                        print "[me] psst, you gotta pick a name, dude\a"
                elif command == "/quit":
                    print "oh no" #oh no
                    quit()
                elif command == "/becomegod":
                    if args:
                        sendmess(message)
                    else:
                        print "[me] I think you need a password...\a"
                elif command == "/alerts":
                    alertson = not alertson
                    print "[me] Most alerts are now turned " + onoff(alertson) #toggle
                elif command == "/help":
                    print "[me] Some commands are available:\n/iam [username] - change your name\n/quit - leave the server\n/alerts - toggle the alerts\n/timestamps - toggle the timestamps\n/help - display this message\n/clear - clear the screen\n/becomegod - ASCEND"
                    #looks crap, still works
                elif command == "/timestamps":
                    timestamps = not timestamps
                    print "[me] Most timestamps are now turned " + onoff(timestamps) 
                elif command == "/clear":
                    print '\033[2J' #special character which clears the terminal
                else:
                    print "[me] That command doesn't exist, try again genius\a"
                args = None
            else:
                sendmess(message)
                sys.stdout.write("\033[F") # delete stuff the user typed
                if timestamps == True:
                    sys.stdout.write(datetime.datetime.now().strftime("%X")[:-3] + ":" + str(datetime.datetime.now().strftime("%S")) + " ") #that's the time
                if isgod == True:
                    sys.stdout.write("[you] ")
                else:
                    sys.stdout.write("<You> ")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()
