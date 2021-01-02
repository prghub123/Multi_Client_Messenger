import socket 
import select 
import threading 

# Defines localhost, Port number, and number of bytes for messages sent/received 
# Same values as server 
HOST = '127.0.0.1' #localhost 
PORT = 55555
NUM_BYTES = 1024 

# Creates Socket for client 
# Uses Internet IPV4 socket/Streaming socket 
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creates alias for the new client 
def create_alias():
    alias = input("Type a Nickname: ")
    return alias 
"""
# Initalizes the client connection
# Params: host address and the port number  
def init_connection(host, port):
    #creates socket for client 
    socket = create_socket() 
    #connecting client to server (localhost and port number) 
    socket.connect((HOST, PORT)) 
""" 
# Handles received messages for client 
# Params: client socket object, number of bytes for message, alias of client 
def receive(client, num_bytes, alias):
    while True:
        try:
            message = client.recv(num_bytes).decode("ascii")
            if message == "NICK":
                client.send(alias.encode("ascii"))
            else:
                print(message)
        except:
            print("An error has occurred! Closing connection...")
            #Closes connection to server for specific client 
            client.close() 
            break 

# Handles messages written by client 
# Params: client socket object, alias of client, number of bytes (probably not necessary)
def write(client, num_bytes, nickname): 
    while True:
        message = f'{nickname}: {input("Message: ")}'
        client.send(message.encode("ascii"))

# Main driver function for handling of client
def main():
    #creates socket object alias for client 
    client_socket = create_socket()
    nick_name = create_alias()
    #establishes connection to server for specific client socket 
    client_socket.connect((HOST, PORT))
    #creates thread for receiving messages and starts the thread for specific client 
    receive_thread = threading.Thread(target=receive, args=(client_socket, NUM_BYTES, nick_name))
    receive_thread.start() 
    #creates thread for writing messages (by client) and starts the thread for specific client 
    write_thread =threading.Thread(target=write, args= (client_socket, NUM_BYTES, nick_name))
    write_thread.start() 


if __name__ == "__main__":
    main() 