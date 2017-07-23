import socket, sys, threading, queue, os
from encryption import *

def receive(connection, privk=None):
    message = connection.recv(3)
    if not message:
        raise ConnectionError("Connection ended")
        os._exit(0)

    remaining = int(message.decode())
    message = b''

    try:
        while remaining > 0:
            r = connection.recv(min(remaining, 16))
            #print("received next chunk: " + str(r))
            message += r
            remaining -= 16
    except Exception as e:
        print(e)
        os._exit(0)

    if privk:
        #print(message)
        return RSA_decrypt(privk, message).encode()
    else:
        return message

def send(connection, message, pubk=None):
    if pubk:
        if len(message) <= 128:
            encrypted = RSA_encrypt(pubk, message.decode())
            connection.sendall(str(len(encrypted)).zfill(3).encode())
            connection.sendall(encrypted)
        else:
            raise ValueError("Size of message to be encrypted is too large")
    else:
        if len(message) < 999:
            connection.sendall(str(len(message.decode())).zfill(3).encode())
            connection.sendall(message)
        else:
            raise ValueError("Size of message to be sent is too large")

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

def get_message(sock, privk):
    while True:
        try:
            print(receive(sock, privk).decode())
        except ConnectionError:
            print("GET_MESSAGE SOCKET CLOSED")
            os._exit(0)

print("Generating keys...")
pubk, privk = generate_RSA_keypair()
print("Key pair generated\n")

if input("Server? (1 or 0): ").strip() == "1":
    print("Server\n")

    sock = socket.socket()
    #server_address = (input("IP: "), int(input("Port: ")))
    server_address = ("localhost", 80)
    print("\nStarting server on {0}:{1}".format(*server_address))
    sock.bind(server_address)

    sock.listen(1)
    cpubk = None

    while not cpubk:
        print("Waiting for a connection...")
        connection, client_address = sock.accept()

        if input("\nConnection from {0}:{1}, type 'accept' to accept: ".format(client_address[0], client_address[1])).strip() == "accept":
            print("Accepted connection from {0}".format(client_address))

            # Exchange keys
            send(connection, str(pubk.key.n).encode())
            send(connection, str(pubk.key.e).encode())
            cpubk = RSA.construct((int(receive(connection).decode()), int(receive(connection).decode())))

        else:
            print("Declined connection from {0}".format(client_address))
            connection.close()

    # Start thread that handles the client's communication with us
    #client_thread = threading.Thread(target = handle_client, args = (connection, client_address))
    #client_thread.daemon = True
    #client_thread.start()

    # Handle our side of the conversation
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    receive_thread = threading.Thread(target=get_message, args=(connection, privk))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        try:
            message = ""

            while not input_queue.empty():
                message += input_queue.get()

            if(message != ""):
                send(connection, message.encode(), cpubk)

        except ConnectionError:
            break

    print("Connection ended, closing server")
    sock.close()

else:
    print("Client\n")

    sock = socket.socket()
    #server_address = None
    server_address = ("localhost", 80)
    while not server_address:
        potential = (input("IP: "), int(input("Port: ")))
        if input("\nYou entered {0}:{1}\nType 'yes' to confirm: ".format(*potential)).strip() == 'yes':
            server_address = potential
        else:
            print("\n")

    print("\nConnecting to {0}:{1} ...".format(*server_address))
    sock.connect(server_address)

    try:
        cpubk = RSA.construct((int(receive(sock).decode()), int(receive(sock).decode())))
        send(sock, str(pubk.key.n).encode())
        send(sock, str(pubk.key.e).encode())
        print("Connected\n")
    except:
        raise ConnectionError("Server refused connection")

    # Start thread that handles the client's communication with us
    #client_thread = threading.Thread(target = handle_client, args = (connection, client_address))
    #client_thread.daemon = True
    #client_thread.start()

    # Handle our side of the conversation
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    receive_thread = threading.Thread(target=get_message, args=(sock, privk))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        try:
            message = ""

            while not input_queue.empty():
                message += input_queue.get()

            if(message != ""):
                send(sock, message.encode(), cpubk)

        except ConnectionError:
            break

    print("Connection ended, closing client")
    sock.close()

'''
Generate key pair

Server:
    Launch server
    Wait for client
    When client joins, ask to accept
    If accepted, exchange key information (receive then send)
    After that, run separate threads for IO
    If client leaves, crash

Client:
    Connect to a server
    If accepted, exchange key information (send then receive)
    After that, run seperate threads for IO
    If server ends, crash
'''
