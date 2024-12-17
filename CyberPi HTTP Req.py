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
    sock.connect(("jsonplaceholder.typicode.com", 80))
    
    # Send a properly formatted GET request
    request = (
        "GET /todos/1 HTTP/1.1\r\n"
        "Host: jsonplaceholder.typicode.com\r\n"
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
    
    # Show the response on CyberPi's display
    cyberpi.display.show_label(display_text, 12, "center", index=1)

def socket_get_v2():
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    sock.connect(("themealdb.com", 80))
    
    # Send a properly formatted GET request
    request = (
        "GET /api/json/v1/1/search.php?s=Nasi HTTP/1.1\r\n"
        "Host: themealdb.com\r\n"
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
    
    # Show the response on CyberPi's display
    cyberpi.display.show_label(display_text, 12, "center", index=1)

gettingConnection()

@event.is_press('a')
def is_btn_press():
    # host = "www.themealdb.com"
    # path = "/api/json/v1/1/search.php?s=Nasi"

    socket_get_v2()

@event.is_press('middle')
def is_joy_press():
    socket_get()

@event.is_press('b')
def is_btn_press():
    cyberpi.console.clear()
