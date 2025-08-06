import socket
import sys

try:
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    message = sys.argv[3]
except IndexError:
    print("Usage: client.py <server_host> <server_port> <message>")
    sys.exit(1)

# Init socket
s = socket.socket(type=socket.SOCK_STREAM)
s.connect((server_host, server_port))
s.sendall(message.encode())
print(f"Sent message: {message}, to {server_host}, {server_port}")

# Receive response
received_message = s.recv(2048)
print(
    f"Received message: {received_message.decode()}, from {server_host}, {server_port}"
)

s.close()
