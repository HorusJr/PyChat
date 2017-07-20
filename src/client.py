import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket ot the port where the server is listening
server_address = ('localhost', 10000)
print("Connecting to {0}:{1}".format(*server_address))
sock.connect(server_address)

try:
    # Send data
    message = "This is a message. It will be repeated."
    print("Sending: {}".format(message))
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print("Received: {}".format(data.decode()))

finally:
    print("Closing socket")
    sock.close()
