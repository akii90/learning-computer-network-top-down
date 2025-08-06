import socket
import sys

try:
    server_port = int(sys.argv[1])
except IndexError:
    print("Usage: server.py <listening_port>")
    sys.exit(1)

# Init socket
s = socket.socket(type=socket.SOCK_STREAM)
s.bind(("", server_port))
# Specify listen mode and backlog length
s.listen(50)
print("Server is ready to receive")

while True:
    # Receive request
    connection_socket, sender_address = s.accept()
    received_message = connection_socket.recv(2048)
    print(
        f"Got message: {received_message.decode()}, from {sender_address[0]}, {sender_address[1]}"
    )
    # Receive response
    connection_socket.sendall(received_message.upper())
    print(
        f"Sent message: {received_message.upper().decode()}, to {sender_address[0]}, {sender_address[1]}"
    )
    connection_socket.close()
