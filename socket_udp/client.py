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
s = socket.socket(type=socket.SOCK_DGRAM)
s.sendto(message.encode(), (server_host, server_port))
print(f"Sent message: {message}, to {server_host}, {server_port}")

# Receive response
received_message, sender_address = s.recvfrom(2048)
print(f"Received message: {received_message.decode()}, from {sender_address[0]}, {sender_address[1]}")

s.close()
