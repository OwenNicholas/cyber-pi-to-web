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

def socket_get(host, route, query, parsing):
     # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        sock.connect((str(host), str(route)))
    except OSError as e:
    # Handle connection errors
        error_message = "Connection Error: " + str(e)
        cyberpi.display.show_label(error_message, 12, "center", index=1)
        return  # Exit the function early if connection fails 
    
    # Send a properly formatted GET request
    request = (
        "GET " + str(query) + " HTTP/1.1\r\n"
        "Host: "+ str(host) + "\r\n"
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

    # Parse JSON body with ujson
    try:
        # Display a readable portion of the response body
        if len(body) > 100:  # Limit to 100 characters for display
            display_text = body[:100] + "..."
        else:
            display_text = body
        data = ujson.loads(body)  # Parse JSON string into Python dictionary
        # Extract specific fields from the JSON response
        requestData = data.get(str(parsing), "Check Your Req")
        # completed = data.get("completed", "No Status")
        display_text = requestData
    except ValueError:
        display_text = "Error parsing JSON"
    
    # Show the response on CyberPi's display
    cyberpi.display.show_label(display_text, 12, "center", index=1)

def socket_post(host, route, query, data):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        sock.connect((str(host), str(route)))
    except OSError as e:
    # Handle connection errors
        error_message = "Connection Error: " + str(e)
        cyberpi.display.show_label(error_message, 12, "center", index=1)
        return  # Exit the function early if connection fails 
    

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

def socket_put(host, route, query, data):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        sock.connect((str(host), str(route)))
    except OSError as e:
    # Handle connection errors
        error_message = "Connection Error: " + str(e)
        cyberpi.display.show_label(error_message, 12, "center", index=1)
        return  # Exit the function early if connection fails 

    # Hardcoded JSON data for the PUT request
    json_data = str(data)
    content_length = str(len(json_data))  # Convert content length to a string

    # Build the static HTTP PUT request using concatenation
    request = (
        "PUT "+ query +" HTTP/1.1\r\n"
        "Host: "+ host +"\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + content_length + "\r\n"
        "Connection: close\r\n\r\n" +
        json_data
    )

    # Send the PUT request
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

def socket_patch(host, route, query, data):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        sock.connect((str(host), str(route)))
    except OSError as e:
    # Handle connection errors
        error_message = "Connection Error: " + str(e)
        cyberpi.display.show_label(error_message, 12, "center", index=1)
        return  # Exit the function early if connection fails 

    # Hardcoded JSON data for the PATCH request
    json_data = str(data)
    content_length = str(len(json_data))  # Convert content length to a string

    # Build the static HTTP PATCH request using concatenation
    request = (
        "PATCH "+ query +"HTTP/1.1\r\n"
        "Host: "+ host +"\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + content_length + "\r\n"
        "Connection: close\r\n\r\n" +
        json_data
    )

    # Send the PATCH request
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
    host = "192.168.18.244"
    route = "80"
    query = "/get_message/3"
    parsing = "content"
    socket_get(host, route, query, parsing)

@event.is_press('up')
def is_joy_press():
    host = "192.168.18.244"
    route = "80"
    query = "/send_message"
    data = '{"content" : "Ahayyyyy"}'
    socket_post(host, route, query, data)

@event.is_press('b')
def is_btn_press():
    cyberpi.console.clear()