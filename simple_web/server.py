import socket
import sys


def generate_headers_list(status_code, status_info):
    headers_list = [
        f"HTTP/1.1 {status_code} {status_info}\r\n",
        "Content-Type: text/html; charset=UTF-8\r\n",
        "\r\n",
    ]
    return headers_list


# Parse arg
try:
    server_port = int(sys.argv[1])
except IndexError:
    print("Usage: server.py <listening_port>")
    sys.exit(1)

# Prepare a sever socket
listening_socket = socket.socket(type=socket.SOCK_STREAM)
listening_socket.bind(("", server_port))
listening_socket.listen(50)

while True:
    # Establish the connection
    print("Ready to serve...")
    connection_socket, addr = listening_socket.accept()
    try:
        message = connection_socket.recv(2048)
        url = message.split()[1]
        # There are Path Traversal defenses in real http server.
        if url == b"/":
            requested_file = "index.html"
        else:
            requested_file = url.decode().removeprefix("/")
        f = open(requested_file)
        response_body = f.read()
        f.close()
        # Send HTTP header line
        headers = generate_headers_list(200, "OK")
        for header in headers:
            connection_socket.send(header.encode())
        # Send the content of the requested file to the client
        connection_socket.sendall(response_body.encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close()
    except IOError:
        # Send response message for file not found
        f = open("404.html")
        response_body = f.read()
        f.close()
        headers = generate_headers_list(404, "Not Found")
        for header in headers:
            connection_socket.send(header.encode())
        connection_socket.sendall(response_body.encode())
        connection_socket.send("\r\n".encode())
        # Close client socket
        connection_socket.close()
