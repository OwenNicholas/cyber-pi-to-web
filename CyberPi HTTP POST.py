import socket
import event, time, cyberpi
import ujson

ssid="Cyberspace"
pasw="#bestinclass"

def gettingConnection():
    try:
        cyberpi.display.show_label("Socket Testing", 12, "top_mid", index= 0)
        cyberpi.wifi.connect(ssid, pasw)
        cyberpi.display.show_label("Connected to WiFi", 12, "center", index= 1)
    except:
        cyberpi.display.show_label("Connection Failed", 12, "center", index= 1)

def socket_post(host, route, query, data):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        cyberpi.display.show_label("Connecting to Server...", 12, "top_mid", index= 0)
        sock.connect((str(host), str(route)))
    except OSError as e:
    # Handle connection errors
        error_message = "Connection Error: " + str(e)
        cyberpi.display.show_label(error_message, 12, "center", index=1)
        return  # Exit the function early if connection fails 
    
    cyberpi.display.show_label("Connected to Server", 12, "top_mid", index= 0)

    # Hardcoded JSON data for the POST request
    json_data = str(data)
    content_length = str(len(json_data))  # Convert content length to a string

    # Build the static HTTP POST request using concatenation
    request = (
        "POST "+ query +" HTTP/1.1\r\n"
        "Host: " + host + "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + content_length + "\r\n"
        "Connection: close\r\n\r\n" +
        json_data
    )

    # Send the POST request
    cyberpi.display.show_label("Try to POST Request", 12, "center", index= 1)
    sock.send(request.encode('utf-8'))

    # Receive the response
    response = b""

    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    # Close the socket
    sock.close()

    # Decode the response and split headers and body
    response_text = response.decode('utf-8')
    headers, body = response_text.split("\r\n\r\n", 1)

    # Display the raw response body on CyberPi
    cyberpi.display.show_label(body, 12, "center", index=1)

gettingConnection()

@event.is_press('a')
def is_joy_press():
    host = "192.168.18.79"
    route = "8080"
    query = "/send_message"
    data = '{"sensor": "dht11", "value" : "66"}'
    socket_post(host, route, query, data)