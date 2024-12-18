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

def socket_get():
     # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect(("192.168.18.244", 8080))
    
    # Send a properly formatted GET request
    request = (
        "GET /get_message/5 HTTP/1.1\r\n"
        "Host: 192.168.18.244\r\n"
        "Connection: close\r\n\r\n"
    )
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
    
    # Display a readable portion of the response body
    if len(body) > 100:  # Limit to 100 characters for display
        display_text = body[:100] + "..."
    else:
        display_text = body

    # Parse JSON body with ujson
    # try:
    #     data = ujson.loads(body)  # Parse JSON string into Python dictionary
    #     # Extract specific fields from the JSON response
    #     title = data.get("content", "No Title")
    #     # completed = data.get("completed", "No Status")
    #     display_text = title
    # except ValueError:
    #     display_text = "Error parsing JSON"
    
    # Show the response on CyberPi's display
    cyberpi.display.show_label(display_text, 12, "center", index=1)

def socket_post():
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect(("192.168.18.244", 8080))

    # Hardcoded JSON data for the POST request
    json_data = '{"content": "HALOK"}'
    content_length = str(len(json_data))  # Convert content length to a string

    # Build the static HTTP POST request using concatenation
    request = (
        "POST /send_message HTTP/1.1\r\n"
        "Host: 192.168.18.244\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + content_length + "\r\n"
        "Connection: close\r\n\r\n" +
        json_data
    )

    # Send the POST request
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
    cyberpi.display.show_label(body[:100] + "...", 12, "center", index=1)

gettingConnection()

@event.is_press('a')
def is_joy_press():
    socket_get()

@event.is_press('up')
def is_joy_press():
    socket_post()

@event.is_press('b')
def is_btn_press():
    cyberpi.console.clear()
