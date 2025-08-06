import socket
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
server_socket = socket.socket(type=socket.SOCK_STREAM)
# Fill in start.
# Fill in end.

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    print('Received a connection from:', addr)
    message = # Fill in start. # Fill in end.
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    file_exist = "false"
    file_touse = "/" + filename
    print(file_touse)

    try:
        # Check whether the file exist in the cache
        f = open(file_touse[1:], "r")
        output_data = f.readlines()
        file_exist = "true"
        # Proxy server finds a cache hit and generates a response message
        connection_socket.send("HTTP/1.0 200 OK\r\n")
        connection_socket.send("Content-Type:text/html\r\n")
        # Fill in start.
        # Fill in end.
        print('Read from cache')
        # Error handling for file not found in cache
    except IOError:
        if file_exist == "false":
            # Create a socket on the proxy server
            c = # Fill in start. # Fill in end.
            hostname = filename.replace("www.","",1)
            print(hostname)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                file_object = c.makefile('r', 0)
                file_object.write("GET " + "http://" + filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                # Fill in start.
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmp_file = open("./" + filename,"wb") # Fill in start.
                # Fill in end.
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            # Fill in end.
    # Close the client and the server sockets
    connection_socket.close()
# Fill in start.
# Fill in end.