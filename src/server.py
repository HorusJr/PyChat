import socket
import sys
import threading

def broadcast(message):
    global clients
    for connection in clients:
        connection.sendall(message)

def handle_client(connection, client_address):
    global clients
    print("Connection from {}".format(client_address))

    try:
        name = connection.recv(16)
        clients[connection] = name
        connection.sendall("Welcome, {0}".format(name))
    except:
        #connection.close()
        pass

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        if not data:
            break
        print("\nReceived {}".format(data.decode()))
        print("Broadcasting")
        #connection.sendall(data)
        broadcast(data)

    connection.close()
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
