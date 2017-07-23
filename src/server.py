import socket
import sys
import threading

def receive(connection):
    message = connection.recv(3)
    if not message:
        raise ConnectionError("Connection ended")

    remaining = int(message.decode())
    message = ""
    while remaining > 0:
        message += connection.recv(min(remaining, 16)).decode()
        remaining -= 16

    return message.encode()

def send(connection, message):
    if(len(message) <= 999):
        connection.sendall(str(len(message.decode())).zfill(3).encode())
        connection.sendall(message)
    else:
        raise ValueError("Size of message sent is over 999")

def broadcast(sender, message):
    global clients
    for connection in clients:
        if connection != sender:
            send(connection, message)

def greeting(connection):
    global clients
    print("Connection from {}".format(client_address))

    name = receive(connection).decode()
    clients[connection] = name
    send(connection, "Welcome, {0}".format(name).encode())

def handle_client(connection, client_address):
    print("Connection from {}".format(client_address))

    name = receive(connection).decode()
    clients[connection] = name
    send(connection, "Welcome, {0}".format(name).encode())

    # Receive the data in small chunks and retransmit it
    while True:
        try:
            message = receive(connection)
            print("\nReceived {}".format(message.decode()))
            broadcast(connection, (name + ": " + message.decode()).encode())
            send(connection, (name + ": " + message.decode()).encode())
        except ConnectionError:
            break

    connection.close()
    del clients[connection]
    print("No more data from {}".format(client_address))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print("Starting up on {0}:{1}".format(*server_address))
sock.bind(server_address)

sock.listen(1)
clients = {}

while True:
    print("Waiting for a connection")
    connection, client_address = sock.accept()
    threading.Thread(target = handle_client, args = (connection, client_address,)).start()
