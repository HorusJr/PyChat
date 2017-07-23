import socket
import sys

def receive():
    global sock

    # Get size of incoming message
    message = sock.recv(3)
    if not message:
        raise ConnectionError("Connection ended")

    remaining = int(message.decode())
    message = ""
    while remaining > 0:
        message += sock.recv(min(remaining, 16)).decode()
        remaining -= 16

    return message.encode()

def send(message):
    global sock

    if(len(message) <= 999):
        sock.sendall(str(len(message.decode())).zfill(3).encode())
        sock.sendall(message)
    else:
        raise ValueError("Size of message sent is over 999")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (input("IP Address: "), int(input("Port: ")))
server_address = ("localhost", 10000)
print("Connecting to {0}:{1}\n".format(*server_address))
sock.connect(server_address)

send(input("Name: ").encode())
print(receive().decode())

while True:
    # Send data
    try:
        message = input("Message: ")
        #print("Sending: {}".format(message))
        send(message.encode())
        print(receive().decode())
    except ConnectionError:
        break

print("Closing socket")
sock.close()

# First send name
# Then join chatroom
