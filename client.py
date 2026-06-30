import sys                     # Used for command-line arguments and exiting program
import socket                  # Provides networking/socket functionality
import select as sel           # Used to monitor multiple input sources

# Initially monitor keyboard input (stdin)
SOCKET_LIST = [sys.stdin]

def chat_client():
    # Check whether hostname and port are provided
    if len(sys.argv) < 3:
        print("Usage: python3 {} hostname port".format(sys.argv[0]))
        #sys.exit(-1)

    # Read hostname from command line
    host = sys.argv[1]
    # Read port number from command line
    port = int(sys.argv[2])

    # Create TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set connection timeout to 5 seconds
    s.settimeout(5)

    # Remote connection
    # Try connecting to server
    try:
        s.connect((host, port))
    except:
        print("Cannot reach the {}:{}".format(host, port))
        sys.exit(-1)

    print("Connected to remote host. You can start sending to messages...")
    # Display prompt
    sys.stdout.write("> ")
    sys.stdout.flush()

    while True:

        # Wait until there is activity on monitored objects
        read_ready, write_ready, error = sel.select(SOCKET_LIST, [], [])
        # Block until connection is made

        # Process each ready object
        for sock in read_ready:
            # If activity came from socket
            if sock == s:
                # Receive data from server
                data = data.recv(4024)
                # If server disconnected
                if not data:
                    print("chat disconnected")
                    sys.exit()
                else:
                    # Display received message
                    sys.stdout.write(data)
                    # Show prompt again
                    sys.stdout.write("> ")
                    sys.stdout.flush()

            # If activity came from keyboard
            else:
                # Read user input
                msg = sys.stdin.readline()

                # Send message to server
                s.send(msg.encode())

                # Show prompt again
                sys.stdout.write("> ")

                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())