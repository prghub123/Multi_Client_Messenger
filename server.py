import socket 
import select 
import threading 
import time 

#Defines localhost, Port number, and number of bytes for messages sent/received 
HOST = '127.0.0.1' #localhost 
PORT = 55555
NUM_BYTES = 1024 

#Lists to hold client IDs and nick names for each client 
clientList = []
nickNames = [] 

# Creates socket for server 
# Creates Internet Socket (IPV4); creates STREAM socket 
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" will probably have all of this code running in main driver function 
# Initializes Socket Connection 
# Params:HOST IP; PORT NUMBER 
def init_connection(host, port):
    #creates socket object 
    socket = create_socket() 
    #binds socket to known host and port 
    socket.bind((host, port))
    #socket now looks for incoming connections 
    socket.listen()

"""
# Broadcast message to every client in the server 
# Params: message being broadcasted  
def broadcast(message):
    for client in clientList:
        client.send(message) 

# Receive message from client and broadcast to other clients 
# Params: client being serviced; number of bytes per message (default 1024)   
def handle(client, num_bytes): 
    while True: 
        # if message can be attained, receive it and broadcast it to other clients 
        try:
            message = client.recv(num_bytes) 
            broadcast(message)
        # if message cannot be received, end connection for the specific client 
        # Remove client from clientList and remove nick name from nickName list  
        except: 
            index = clientList.index(client)
            clientList.remove(client) 
            client.close() 
            nickname = nickNames[index]
            broadcast(f"{nickname} has left the chat. Goodbye!".encode("ascii")) 
            nickNames.remove(nickname)
            break 

# Establishes connection of client connecting to server 
# Params: the server socket 
def receive(server_socket, num_bytes):
    while True:
        # provides the client ID and the address of the client socket 
        client, addr = server_socket.accept() 
        print(f"Connected with {str(addr)}")
        # sends keyword to client to get nickname of client 
        client.send("NICK".encode("ascii"))
        # after handshake is established, client will send nickname back to server 
        nickname = client.recv(num_bytes).decode("ascii")
        # adds nick name to nickName list and client to client list 
        nickNames.append(nickname)
        clientList.append(client)
        # prints welcome messages for new client 
        print(f"Nick-Name of new client is {nickname}.")
        broadcast(f"{nickname} has joined the chat. Welcome!".encode("ascii"))
        client.send("You have connected to the server".encode("ascii"))
        # define and run a thread for each client that is connected to the server 
        thread = threading.Thread(target=handle, args=(client,num_bytes))
        thread.start() 


# Main driver function for server
# Takes care of initializing connections and establishing connections with clients 
def main():
    socket = create_socket()
    socket.bind((HOST, PORT))
    socket.listen() 
    print("Server is Listening....")
    receive(socket, NUM_BYTES)


if __name__ == "__main__":
    main()  