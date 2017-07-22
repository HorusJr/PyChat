import socket
import sys

def receive(sock, amount_expected):
    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    data = b''
    while amount_received < amount_expected:
        data += sock.recv(16)
        amount_received += len(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return data

server_address = (input("IP Address: "), int(input("Port: ")))
print("Connecting to {0}:{1}\n".format(*server_address))
sock.connect(server_address)

name = input("Name: ")
sock.sendall(name.encode())

while True:
    # Send data
    message = input("Message: ")
    print("Sending: {}".format(message))
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    data = b''
    while amount_received < amount_expected:
        data += sock.recv(16)
        amount_received += len(data)
    print("Received: {}".format(receive(sock, ))

    print("Closing socket")
    sock.close()

# First send name
# Then join chatroom
