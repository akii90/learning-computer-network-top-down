import socket
import sys
import time

server_port = 12000
ttl = 1

try:
    server_host = sys.argv[1]
    packet_count = int(sys.argv[2])
    ttl = int(sys.argv[3])
except IndexError:
    print("Usage: client.py <server_host> <packet_count> <ttl(s, default 1)>")
    sys.exit(1)

message = "ping packet"

s = socket.socket(type=socket.SOCK_DGRAM)
s.settimeout(ttl)
print("Ready to send packets")

for sequence_number in range(1, packet_count + 1):
    try:
        s.sendto(message.encode(), (server_host, server_port))
        sending_time = time.time()
        receiving_message, address = s.recvfrom(2048)
        receiving_time = time.time()
        rtt = (receiving_time - sending_time) * 1000
        print(f"Ping Seq{sequence_number} time={rtt:.3f}ms")
    except TimeoutError as e:
        print(f"Ping Seq{sequence_number} request timed out")

s.close()
