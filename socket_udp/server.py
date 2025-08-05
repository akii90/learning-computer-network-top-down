import socket
import sys

try:
    server_port = int(sys.argv[1])
except IndexError:
    print("Usage: server.py <listening_port>")
    sys.exit(1)

# Init socket
s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(('', server_port))
print("Server is ready to receive")

while True:
    # Receive request
    received_message, sender_address = s.recvfrom(2048)
    print(f"Got message: {received_message.decode()}, from {sender_address[0]}, {sender_address[1]}")
    # Receive response
    s.sendto(received_message.upper(), sender_address)
    print(f"Sent message: {received_message.upper().decode()}, to {sender_address[0]}, {sender_address[1]}")

