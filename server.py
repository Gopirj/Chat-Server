import socket as s
import select as sel
import sys

HOST=''                    # Listen on all available network interfaces
PORT=4444                  # Port number on which server will listen
SOCKET_LIST = []           # Stores server socket and all connected client sockets
RECEIVE_BUFF=4096          # Maximum bytes received at a time


def chat_server():
    # Create TCP socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM) #s.socket(AF-(address_family),continue stream)
    # Allow reuse of the same address/port after restart
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1) #(SOL_SOCKET-(layer),address,value)
    # Bind socket to host and port
    server_socket.bind((HOST, PORT)) #bind - this go to that particular place
    # Listen for incoming connections
    server_socket.listen(100) #listen - listen to a comes signal
    # Add server socket to monitoring list
    SOCKET_LIST.append(server_socket)

    print(f"Chat server started on port {PORT}")
    print('Waiting for connection...\n')

    # Infinite loop - server runs continuously
    while True:
        #Blocking the flow for new incoming connection...
        # Wait for activity on any socket and Monitor all sockets in SOCKET_LIST

        # ready_read contains sockets that have activity
        ready_read, ready_write, error = sel.select(SOCKET_LIST,[], [], 0)  #select -  this function file handling process in read able state or write able state going or not workes do check this function

        # Process each socket that has activity
        for sock in ready_read:
            # New connection request
            # If activity is on server socket,
            # it means a new client wants to connect
            if sock == server_socket:
                # Accept client connection
                client_socket, addr = server_socket.accept()

                # Add new client socket to monitoring list
                SOCKET_LIST.append(client_socket)
               # print(addr)
                print("Client {}:{} Connected!".format(addr[0], addr[1]))

                # Notify all other clients
                broadcast(server_socket, client_socket,"{} entered our chatting room..\n".format(addr))

            # Message from existing client
            else:
                try:
                    # Receive data from client
                    data = sock.recv(RECEIVE_BUFF)

                    # Convert bytes to string
                    data = data.decode()

                    # If message exists
                    if data:
                        # Send message to all other clients
                        broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(), data))

                    # Empty message means client disconnected
                    else:
                        #the socket must have been broken, remove the list, and broadcast a message
                        broadcast(server_socket, sock, "[{}] {}".format(sock .getpeername(),"Client is Disconnected\n  "))

                        # Remove client socket
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                except:
                    broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(), "Client is Disconnected\n  "))
                    continue
        #server_socket.close()


def broadcast(server_socket, client_socket, message):
    """
        Send message to all clients except the server
        and the client who sent the message.
        """
    print("Broadcasting message..."+message)

    # Send message to every connected client
    for socket in SOCKET_LIST:

        # Skip server socket and sender socket
        if socket != server_socket and socket != client_socket:
            try:
                # Convert string to bytes and send
                socket.send(message.encode())
            except:
                #it should be a broken connection
                # Close broken connection
                socket.close()

                # Remove broken socket from list
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

# Program execution starts here
if __name__ == '__main__':
    sys.exit(chat_server())