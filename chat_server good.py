import socket
import select
from thread import *
import sys
import random
import re

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(int(raw_input("Pick max connections ")))
#choose your own max client number
list_of_clients=[]
thepasscode = random.randint(0,9999)
print "The passcode is " + str(thepasscode) #sets a passcode used to become god
maxlen = 16 #the max length of the username, that is

def clientthread(conn, addr):
    conn.send("Welcome to the cool zone")
    #sends the totally cool opening message 
    clientname = "<" + addr[0] + ">" #you gotta set the name just in case
    message = conn.recv(2048)
    if message.split(None, 1)[0] == "/iwasalways": #should be sent by client
        if len(message.split(None, 1)) == 2: #I can't even remember what this bit does
            args = re.sub('[^a-zA-Z0-9_\\ ]', '', message.split(None, 1)[1]) #properly sets the username
            if args.lower() == "god":
                conn.send("[god] No you're not!")
                clientname = addr[0]
            else:    
                clientname = "<" + args[:maxlen] + ">"
        broadcast("[god] " + clientname[1:-1] + " has just joined", conn) #sends joining message
    else:
        remove(conn)
    while True:
        try:     
            message = conn.recv(2048)    
            if message:
                if message[:1] == "/": #checks if it's a command
                    command = message.split(None, 1)[0] #command is now the command
                    try:
                        args = re.sub('[^a-zA-Z0-9_\\ ]', '', message.split(None, 1)[1])
                    except:
                        pass
                    if command == "/iam":
                        if args != None and args != "god": 
                            newname = "<" + args[:maxlen] + ">"
                            broadcast("[god] Turns out " + clientname[1:-1] + " is actually " + args[:maxlen],conn) #renaming
                            clientname = newname #clientname is the username of the client, duh.
                        elif args.lower() == "god":
                            conn.send("[god] Hey, no doppleganging")
                        else:
                            conn.send("[me] You gotta pick a name, dude")
                    elif command == "/quit":
                        break #You know, so it quits
                    elif command == "/becomegod":
                        if int(args) == thepasscode:
                            conn.send("[god] Wow, nice guess. Now you can type as me!")
                            broadcast("[god] " + clientname[1:-1] + " HAS ASCENDED!", conn)
                            clientname = "[god]" #becoming god business
                        else:
                            conn.send("[god] Wow, nice guess. jk, you were totally wrong")
                    else:
                        conn.send("[me] That command doesn't exist, try again")
                    args = None #resets args for next command
                else:
                    broadcast(clientname + " " + message,conn) #sends message + username out to the world
            else:
                remove(conn)
        except:
            continue # uhhhhh
    broadcast("[god] " + clientname[1:-1] + " has left",conn) #disconnect message
    print(addr[0] + " disconnected") # private disconnect message
    return(None) #Prevents battery roasting
    conn.send("TIME TO DIE BEPIS MC WEPIS")

def broadcast(message,connection):
    message = message.strip("\n")
    print message
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

print("Now listening for connections to " + str(IP_address) + " on port " + str(Port))
while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print addr[0] + " connected" # connection message
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates an individual thread for every user that connects

conn.close()
server.close()
