import socket
import cyberpi

# Setup Wi-Fi connection
while not cyberpi.wifi.is_connect():
    cyberpi.wifi.connect("Cyberspace", "#bestinclass")
    cyberpi.console.println("Connecting to Wi-Fi...")
cyberpi.console.println("Wi-Fi connected!")

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "192.168.4.1"
server_port = 5050  # Port for the server to listen on
server_socket.bind((str(server_ip), str(server_port)))
server_socket.listen(1)

cyberpi.console.println("Server running at "+ server_ip + ":" + str(server_port))

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    cyberpi.console.println("Connection from " + client_address)

    # Receive a message
    data = client_socket.recv(1024).decode('utf-8')
    cyberpi.console.println("Received: " + data)

    # Respond to the client
    if data == "request":
        response = "Hello from Server!"
        client_socket.send(response.encode('utf-8'))
        cyberpi.console.println("Response sent!")

    # Close the client socket
    client_socket.close()
