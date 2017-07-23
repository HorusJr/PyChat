import socket
import sys
import queue
import threading

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

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
server_address = ("71.68.222.92", 80)
print("Connecting to {0}:{1}\n".format(*server_address))
sock.connect(server_address)

send(input("Name: ").encode())
print(receive().decode())

input_queue = queue.Queue()
input_thread = threading.Thread(target=add_input, args=(input_queue,))
input_thread.daemon = True
input_thread.start()

while True:
    # Send data
    try:
        message = ""

        while not input_queue.empty():
            message += input_queue.get()
            print("Message: " + message)

        print("Sending: {}".format(message))

        if(message != ""):
            send(message.encode())

        print(receive().decode())
    except ConnectionError:
        break

print("Closing socket")
sock.close()

# First send name
# Then join chatroom
