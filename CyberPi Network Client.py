import socket
import cyberpi
import time

# Setup Wi-Fi connection
while not cyberpi.wifi.is_connect():
    cyberpi.wifi.connect("Cyberspace", "#bestinclass")
    cyberpi.console.println("Connecting to Wi-Fi...")
cyberpi.console.println("Wi-Fi connected!")

# Define the server address
server_ip = "192.168.4.1"  # Replace with the server's IP address
server_port = 5050

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
cyberpi.console.println("Connecting to server...")
client_socket.connect((server_ip, str(server_port)))
cyberpi.console.println("Connected to server!")

# Send a message
client_socket.send("request".encode('utf-8'))
cyberpi.console.println("Request sent!")

# Wait for the server's response
time.sleep(1)
response = client_socket.recv(1024).decode('utf-8')
cyberpi.console.println("Response: " + response)
cyberpi.display.show_label(response, 12, "center")

# Close the socket
client_socket.close()
