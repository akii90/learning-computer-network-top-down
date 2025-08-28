import os.path
import socket
import sys


def generate_response_headers(status_code, status_info):
    headers_list = [
        f"HTTP/1.1 {status_code} {status_info}\r\n",
        "Content-Type: text/html; charset=UTF-8\r\n",
        "\r\n",
    ]
    return headers_list


def generate_request_headers(domain, file):
    headers_list = [
        f"GET /{file} HTTP/1.1\r\n",
        f"Host: {domain}\r\n",
        "User-Agent: proxy\r\n",
        "\r\n",
    ]
    return headers_list


def is_response_success(response: bytes):
    is_success = False
    if response.split()[1] == b"200":
        is_success = True
    return is_success


def get_response_file(response: bytes):
    return response.split(b"\r\n\r\n")[1]


cache_dir = "/tmp/proxy/"

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
    file_exist = False

    # Strat receiving data from the client
    print("Ready to serve...")
    client_socket, client_addr = server_socket.accept()
    print("Received a connection from:", client_addr)
    client_request = client_socket.recv(4096).decode()
    crude_client_url = client_request.split()[1].removeprefix("/")
    print(f"client request url:{crude_client_url}")

    # Extract target host and requested file
    target_host = crude_client_url.split("/")[0]
    print(f"Target host: {target_host}")
    if len(crude_client_url.split("/")) < 2:
        request_filename = ""
    else:
        request_filename = crude_client_url.removeprefix(target_host + "/")
    print(f"Requested fil: {request_filename}")

    cache_file = cache_dir + target_host + "/" + request_filename

    try:
        # Check whether the file exist in the cache
        with open(cache_file, "r") as f:
            file_content = f.readlines()
            file_exist = True
            # Proxy server finds a cache hit and generates a response message
            request_headers = generate_response_headers(200, "OK")
            for header in request_headers:
                client_socket.send(header.encode())
            for line in file_content:
                client_socket.sendall(line.encode())
            print("Successfully response from cache")
    # Error handling for file not found in cache
    except IOError:
        # Create a socket for target host
        target_sever_socket = socket.socket(type=socket.SOCK_STREAM)
        try:
            print(f"Send request to target host: {target_host}")
            # Connect to target host
            target_sever_socket.connect((target_host, 80))
            # Read the response into buffer
            request_headers = generate_request_headers(target_host, request_filename)
            for header in request_headers:
                target_sever_socket.send(header.encode())

            response_byte = b""
            while True:
                response_chunk = target_sever_socket.recv(4096)
                if not response_chunk:
                    break
                response_byte += response_chunk
            print(f"Response from target host:\n{response_byte}")
            target_sever_socket.close()

            # Response to client and caching file
            client_socket.sendall(response_byte)
            if is_response_success(response_byte):
                response_file = get_response_file(response_byte)
                print(response_file)

                cache_file_subdir = os.path.dirname(cache_file)
                if cache_file_subdir:
                    print("Creating cache sub dir")
                    os.makedirs(cache_file_subdir, exist_ok=True)

                with open(cache_file, "wb") as f:
                    print(f"Caching file from target host: {target_host}")
                    f.write(response_file)
        except Exception as e:
            print("Illegal request")
            print(e)
    # Close the client and the server sockets
    client_socket.close()
