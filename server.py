import socket
import sys
import threading 

def read_msg(clients, sock_cli, addr_cli, src_username):
    #Receive message
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        #parsing pesannya
        dest, msg = data.split(b"|", 1)
        dest = dest.decode("utf-8")

    #send messages to clients
        #send messages to clients (broadcast)
        if dest == "bcast":
            msg = msg.decode("utf-8")
            msg2 = "<{}>: {}".format(src_username, msg)
            send_broadcast(clients, msg2, addr_cli)

        #send private messages
        else:
            msg = msg.decode("utf-8")
            msg2 = "<{}>: {}".format(src_username, msg)
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg2)

    #Disconnect client and removed from client list
    sock_cli.close()
    print("connection closed", addr_cli)
    del clients["{}:{}".format(addr_cli[0], addr_cli[1])]

#send_broadcast(All client)
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        send_msg(sock_cli, data)

#send_msg(messages to specific clients)
def send_msg(sock_cli, data):
    message = f'message|{data}'
    sock_cli.send(bytes(message, "utf-8"))


#Object socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind server ke IP dan port tertentu
server_socket.bind(('127.0.0.1', 6666))

#Server listen
server_socket.listen(5)

#Dictionary untuk client
clients = {}

try:
    while True:
        sock_cli, addr_cli = server_socket.accept()

        #Receive username from client
        src_username = sock_cli.recv(65535).decode("utf-8")
        print(" {} successfully joined".format(src_username))

        #Make Thread
        thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, src_username))
        thread_cli.start()

        #Adding a new client to the dictionary
        clients[src_username] = (sock_cli, addr_cli, thread_cli)

except KeyboardInterrupt:
    #Close the server object
    server_socket.close()
    sys.exit(0)