import socket
import sys


def request():
    pass


def response():
    pass


def generate_response_headers(status_code, status_info):
    headers_list = [
        f"HTTP/1.1 {status_code} {status_info}\r\n",
        "Content-Type: text/html; charset=UTF-8\r\n",
        "\r\n",
    ]
    return headers_list


def generate_request_headers(domain, file):
    headers_list = [
        f"GET /{file} HTTP/1.1\n",
        f"Host: {domain}\n",
        "User-Agent: proxy\n",
        "\r\n",
    ]
    return headers_list


# TODO, response status
def is_response_success{
    pass
}

# class ProxySession:

# cache_dir = /tmp/proxy

try:
    server_port = int(sys.argv[1])
except IndexError:
    print("Usage: http_proxy_server.py <listening_port>")
    sys.exit(1)

# Create a server socket, bind it to a port and start listening
server_socket = socket.socket(type=socket.SOCK_STREAM)
server_socket.bind(("", server_port))
server_socket.listen(50)

while 1:
    # Strat receiving data from the client
    print("Ready to serve...")
    client_socket, client_addr = server_socket.accept()
    print("Received a connection from:", client_addr)
    client_request = client_socket.recv(4096).decode()
    print(f"raw request:\n{client_request}")
    crude_client_url = client_request.split()[1].removeprefix("/")
    print(f"client request url:{crude_client_url}")

    # Extract target host and target resource
    target_host = crude_client_url.split("/")[0]
    print(target_host)
    if len(crude_client_url.split("/")) < 2:
        request_filename = ""
    else:
        request_filename = crude_client_url.split("/")[1]
    print(request_filename)
    file_exist = False

    try:
        # Check whether the file exist in the cache
        with open(request_filename, "r") as f:
            file_content = f.readlines()
            file_exist = True
            # Proxy server finds a cache hit and generates a response message
            request_headers = generate_response_headers(200, "OK")
            for header in request_headers:
                client_socket.send(header.encode())
            for line in file_content:
                client_socket.sendall(line.encode())
            print("Read from cache")
    # Error handling for file not found in cache
    except IOError:
        if not file_exist:
            # Create a socket on the proxy server
            target_sever_socket = socket.socket(type=socket.SOCK_STREAM)
            # hostname = request_filename.replace("www.", "", 1)
            # print(hostname)
            try:
                print(f"Send request to target host: {target_host}")
                # Connect to target host
                target_sever_socket.connect((target_host, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                # file_object = target_sever_socket.makefile("r", 0)
                # file_object.write("GET " + "http://" + request_filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                # Fill in start.
                request_headers = generate_request_headers(
                    target_host, request_filename
                )
                print(f"Headers:\n{request_headers}")
                for header in request_headers:
                    target_sever_socket.send(header.encode())
                response_byte = b""
                while True:
                    response_chunk = target_sever_socket.recv(4096)
                    if not response_chunk:
                        break
                    response_byte += response_chunk
                print(f"Response from target host:\n{response_byte}")
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                client_socket.sendall(response_byte)
                if is_response_success:
                    tmp_file = open("./" + request_filename, "wb")
                # Fill in start.
                client_socket.sendall(response_byte)
                # Fill in end.
            except Exception as e:
                print("Illegal request")
                print(e)
        else:
            # HTTP response message for file not found
            # Fill in start.
            pass
            # Fill in end.
    # Close the client and the server sockets
    client_socket.close()
# Fill in start.
# Fill in end.
