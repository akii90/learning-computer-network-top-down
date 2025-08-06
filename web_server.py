import socket
import sys

server_socket = socket.socket(type=socket.SOCK_STREAM)
# Prepare a sever socket
# Fill in start
# Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connection_socket, addr = # Fill in start # Fill in end
    try:
        message = # Fill in start # Fill in end
        filename = message.split()[1]
        f = open(filename[1:])
        output_data = # Fill in start # Fill in end
        # Send one HTTP header line into socket
        # Fill in start
        # Fill in end
        # Send the content of the requested file to the client
        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close() 
    except IOError:
        # Send response message for file not found
        # Fill in start
        # Fill in end
        # Close client socket
        # Fill in start
        # Fill in end
server_socket.close()
# Terminate the program after sending the corresponding data
sys.exit()
