import socket
import sys
import threading 

def read_msg(sock_cli): 
    #Receive messages
    while True:
        msg = sock_cli.recv(65535)
        if len(msg) == 0:
            break
        datatype, message = msg.split(b"|", 1)
        datatype = datatype.decode("utf-8")

        #print mesaages
        if datatype == "message":
            message = message.decode("utf-8")
            print(message)

#Object socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to server
sock_cli.connect(('127.0.0.1', 6666))

## Fetch username
username = sys.argv[1]
sock_cli.send(bytes(username, "utf-8"))

#create a Thread to receive messages
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

#Send messages
try:
    while True:
        dest = input("-send private messages : chat <username> <message>\n"
                     "-send broadcast : bcast <message>\n"
                     "-exit : exit\n")
        msg = dest.split(" ", 1)

        if msg[0] == "exit":
            sock_cli.close()
            break

        elif msg[0] == "chat":
            username, message = msg[1].split(" ", 1)
            sock_cli.send(bytes("{}|{}".format(username, message), "utf-8"))    
            
        elif msg[0] == "bcast":
            sock_cli.send(bytes("bcast|{}".format(msg[1]), "utf-8"))    

        else:
            print("wrong command")

except KeyboardInterrupt:
    sock_cli.close()
    sys.exit(0)