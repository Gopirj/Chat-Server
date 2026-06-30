# Chat-Server

## Flow Chart

### 1. Server side chat 
```text
┌─────────────────────────┐
│          START          │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Import Required Modules │
│ socket, select, sys     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Initialize Variables    │
│ HOST                    │
│ PORT                    │
│ SOCKET_LIST             │
│ RECEIVE_BUFF            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Create TCP Socket       │
│ socket(AF_INET,         │
│ SOCK_STREAM)            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ setsockopt()            │
│ SO_REUSEADDR = 1        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ bind(HOST, PORT)        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ listen(100)             │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Add Server Socket to    │
│ SOCKET_LIST             │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Print Waiting Message   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       while True        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ select(SOCKET_LIST)     │
│ Wait for Activity       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ ready_read Sockets      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ for sock in ready_read  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ sock == server_socket ? │
└───────┬─────────┬───────┘
         │YES      │NO
         ▼         ▼

┌──────────────────┐   ┌──────────────────┐
│ New Client       │   │ Existing Client  │
│ Connection       │   │ Sent Data        │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│ accept()         │   │ recv()           │
│ Get Client       │   │ Receive Message  │
│ Socket & Address │   └────────┬─────────┘
└────────┬─────────┘            │
         │                      ▼
         ▼            ┌──────────────────┐
┌──────────────────┐  │ decode()         │
│ Add Client to    │  │ Convert Bytes    │
│ SOCKET_LIST      │  │ to String        │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│ Print Client     │  │ Message Exists ? │
│ Connected Msg    │  └───────┬────┬─────┘
└────────┬─────────┘          │YES │NO
         │                    ▼    ▼
         ▼          ┌────────────┐ ┌──────────────┐
┌──────────────────┐│ broadcast()│ │ Client       │
│ broadcast()      ││ Send Msg   │ │ Disconnected │
│ "Entered Chat"   ││ to Others  │ └──────┬───────┘
└────────┬─────────┘└─────┬──────┘        │
         │                │               ▼
         │                │    ┌──────────────────┐
         │                │    │ broadcast()      │
         │                │    │ Notify Others    │
         │                │    └────────┬─────────┘
         │                │             │
         │                │             ▼
         │                │    ┌──────────────────┐
         │                │    │ Remove Client    │
         │                │    │ from SOCKET_LIST │
         │                │    └────────┬─────────┘
         │                │             │
         └────────┬───────┴─────────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Repeat Loop      │
         │ Wait for Next    │
         │ Activity         │
         └────────┬─────────┘
                  │
                  ▼
              while True
```

### Broadcast Function Flow

```text
broadcast(server_socket,
          client_socket,
          message)
            │
            ▼
   for socket in SOCKET_LIST
            │
            ▼
 Is socket != server_socket
 AND
 socket != client_socket ?
            │
      ┌─────┴─────┐
      │           │
     NO          YES
      │           │
      ▼           ▼
    Skip      send(message)
                  │
                  ▼
            Send Success?
                  │
          ┌───────┴───────┐
          │               │
         YES             NO
          │               │
          ▼               ▼
      Continue      close(socket)
                         │
                         ▼
                remove(socket)
                         │
                         ▼
                     Continue
```
              
## Overall Chat Server Architecture Explanation

### Client-Server Architecture

```text
                  ┌─────────────┐
                  │   SERVER    │
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Client 1       Client 2       Client 3
          │              │              │
          └──────┬───────┴───────┬──────┘
                 │               │
                 ▼               ▼
            Message Sent
                 │
                 ▼
             Server recv()
                 │
                 ▼
           broadcast()
                 │
         ┌───────┴────────┐
         ▼                ▼
     Client 2         Client 3
   Receives Msg     Receives Msg
```

### 2. Client side chat 
```text
┌─────────────────────────┐
│          START          │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Import Required Modules │
│ sys, socket, select     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Check Command Line Args │
│ len(sys.argv) < 3 ?     │
└────────────┬────────────┘
             │
      ┌──────┴──────┐
      │             │
     YES            NO
      │             │
      ▼             ▼
┌─────────────────┐  ┌────────────────────┐
│ Print Usage Msg │  │ Read Host & Port   │
└─────────────────┘  └─────────┬──────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │ Create TCP Socket      │
                  │ socket(AF_INET,        │
                  │ SOCK_STREAM)           │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Set Timeout = 5 Sec    │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Connect to Server      │
                  │ s.connect(host,port)   │
                  └───────────┬────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 FAILED             SUCCESS
                    │                   │
                    ▼                   ▼
         ┌─────────────────┐   ┌─────────────────┐
         │ Print Error Msg │   │ Print Connected │
         │ Exit Program    │   │ Message         │
         └─────────────────┘   └────────┬────────┘
                                         │
                                         ▼
                          ┌────────────────────────┐
                          │ Show Prompt ">"        │
                          └───────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      while True         │
                         └───────────┬─────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │ select() Waits for Activity    │
                    │ on stdin and socket            │
                    └──────────────┬─────────────────┘
                                   │
                                   ▼
                     ┌────────────────────────────┐
                     │ Any Input Available ?      │
                     └─────────────┬──────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
        ┌────────────────────┐      ┌────────────────────┐
        │ User Typed Message │      │ Server Sent Msg    │
        │ (stdin ready)      │      │ (socket ready)     │
        └─────────┬──────────┘      └─────────┬──────────┘
                  │                           │
                  ▼                           ▼
        ┌────────────────────┐      ┌────────────────────┐
        │ Read Keyboard Input│      │ Receive Data       │
        │ readline()         │      │ recv()             │
        └─────────┬──────────┘      └─────────┬──────────┘
                  │                           │
                  ▼                           ▼
        ┌────────────────────┐      ┌────────────────────┐
        │ Encode Message     │      │ Data Received ?    │
        │ msg.encode()       │      └─────────┬──────────┘
        └─────────┬──────────┘                │
                  │                  ┌────────┴─────────┐
                  │                  │                  │
                  ▼                 NO                 YES
        ┌────────────────────┐       │                  │
        │ Send to Server     │       ▼                  ▼
        │ s.send()           │ ┌───────────────┐ ┌────────────────┐
        └─────────┬──────────┘ │ Print         │ │ Display Msg    │
                  │            │ Disconnected  │ │ on Screen      │
                  │            │ Exit Program  │ └───────┬────────┘
                  │            └───────────────┘         │
                  ▼                                      ▼
        ┌────────────────────┐              ┌────────────────────┐
        │ Display Prompt ">" │              │ Display Prompt ">" │
        └─────────┬──────────┘              └─────────┬──────────┘
                  │                                   │
                  └───────────────┬───────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Back to select()│
                         └─────────────────┘
```

---

## Step 1: Server Starts

When you run:

```bash
python3 server.py
```

the server:

1. Creates a TCP socket.
2. Binds to port 4444.
3. Starts listening for clients.
4. Waits for incoming connections.

```text
Server Ready
     │
     ▼
Listening on Port 4444
```

---

## Step 2: Clients Connect

When a client runs:

```bash
python3 client.py localhost 4444
```

the client sends a connection request.

Server receives it using:

```python
client_socket, addr = server_socket.accept()
```

Example:

```text
Client 1 Connected
Client 2 Connected
Client 3 Connected
```

The server stores each client socket inside:

```python
SOCKET_LIST
```

Example:

```text
SOCKET_LIST
│
├── server_socket
├── client1_socket
├── client2_socket
└── client3_socket
```

---

## Step 3: select() Monitors All Clients

Instead of creating:

```text
Thread 1 → Client 1
Thread 2 → Client 2
Thread 3 → Client 3
```

your server uses:

```python
select.select()
```

to monitor all sockets simultaneously.

```text
           select()
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
 Client1   Client2    Client3
```

The server waits until any socket becomes active.

---

## Step 4: Client Sends Message

Suppose Client 1 types:

```text
Hello Everyone
```

Flow:

```text
Client 1
    │
    ▼
send()
    │
    ▼
Server
```

Server receives:

```python
data = sock.recv(RECEIVE_BUFF)
```

---

## Step 5: Server Processes Message

Server converts bytes into text:

```python
data.decode()
```

Example:

```text
b'Hello Everyone'
```

becomes:

```text
Hello Everyone
```

---

## Step 6: Broadcast Message

Server calls:

```python
broadcast(server_socket,
          client_socket,
          message)
```

Purpose:

```text
Send message to everyone
except the sender.
```

---

## Step 7: Other Clients Receive

Server sends:

```text
[(127.0.0.1,5001)] Hello Everyone
```

to:

```text
Client 2
Client 3
```

Flow:

```text
           Client 1
               │
               ▼
            Server
               │
      ┌────────┴────────┐
      ▼                 ▼
  Client 2         Client 3
```

---

## Step 8: Client Disconnects

If Client 2 closes:

```text
CTRL + C
```

or disconnects,

```python
recv()
```

returns empty data.

Server:

1. Detects disconnection.
2. Removes socket from `SOCKET_LIST`.
3. Broadcasts disconnect message.

```text
Client 2 Disconnected
```

---

# Complete Data Flow

```text
Client Types Message
         │
         ▼
     send()
         │
         ▼
 ┌─────────────────┐
 │     SERVER      │
 │                 │
 │ recv()          │
 │ decode()        │
 │ broadcast()     │
 └────────┬────────┘
          │
   ┌──────┴──────┐
   ▼             ▼
Client 2     Client 3
 receive      receive
```

---

# Components and Responsibilities

| Component     | Responsibility                     |
| ------------- | ---------------------------------- |
| Server Socket | Accept new client connections      |
| Client Socket | Communicate with a specific client |
| select()      | Monitor multiple sockets           |
| recv()        | Receive data                       |
| send()        | Send data                          |
| broadcast()   | Forward message to all clients     |
| SOCKET_LIST   | Store all active sockets           |

---

# Why `select()` Is Important

Without `select()`:

```text
Server
  │
  ├─ Wait Client 1
  ├─ Wait Client 2
  └─ Wait Client 3
```

The server could block on one client.

With `select()`:

```text
Server
   │
   ▼
select()
   │
   ▼
Check All Clients Together
```

One server process can handle many clients efficiently.

---

### One-Line Summary

**The server acts as a central hub: it accepts client connections, monitors all connected clients using `select()`, receives messages with `recv()`, and distributes them to all other clients through `broadcast()`.**


**Key idea: select() continuously watches all sockets in SOCKET_LIST. When a new client connects, accept() creates a client socket. When a client sends a message, recv() receives it and broadcast() forwards it to all other connected clients.**
