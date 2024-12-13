import cyberpi
import time
import json

# Constants for Wi-Fi and API URLs
WIFI_SSID = "Cyberspace"
WIFI_PASSWORD = "#bestinclass"
POST_URL = "http://192.168.18.244:8080/send_message"
GET_URL = "http://192.168.18.244:8080/get_messages"

# Global variable to store messages
messages = []
current_message_index = 0  # Tracks which message to display next

def connect_to_wifi():
    """Connect CyberPi to a Wi-Fi network."""
    cyberpi.wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    cyberpi.display.clear()
    if cyberpi.wifi.is_connect():
        cyberpi.display.show_label("Wi-Fi Connected", 16)
        time.sleep(2)
    else:
        cyberpi.display.show_label("Wi-Fi Failed", 16)
        time.sleep(2)

def send_message():
    """Send a message to the server."""
    message = "Halo bro!"
    cyberpi.display.clear()
    if cyberpi.wifi.is_connect():
        try:
            payload = json.dumps({"message": message})
            response = cyberpi.http.post(POST_URL, payload)
            if "200" in response:  # CyberPi's HTTP functions return strings, check for "200"
                cyberpi.display.show_label("Message Sent!", 16)
            else:
                cyberpi.display.show_label("Send Failed!", 16)
        except Exception:
            cyberpi.display.show_label("Send Error!", 16)
    else:
        cyberpi.display.show_label("No Wi-Fi!", 16)

def receive_messages():
    """Retrieve messages from the server."""
    global messages
    cyberpi.display.clear()
    if cyberpi.wifi.is_connect():
        try:
            response = cyberpi.http.get(GET_URL)
            if response.startswith("200"):
                # Extract and parse the JSON data from the response
                data_start = response.find("{")
                if data_start != -1:
                    messages = json.loads(response[data_start:])
                    cyberpi.display.show_label("Messages Received!", 16)
                    time.sleep(2)
                    show_received_messages()
                else:
                    cyberpi.display.show_label("No Messages!", 16)
            else:
                cyberpi.display.show_label("Receive Failed!", 16)
        except Exception:
            cyberpi.display.show_label("Receive Error!", 16)
    else:
        cyberpi.display.show_label("No Wi-Fi!", 16)

def show_received_messages():
    """Display the received messages on the screen one by one."""
    global messages
    cyberpi.display.clear()
    if messages:
        for msg in messages:
            cyberpi.display.show_label(msg, 16)
            time.sleep(2)  # Show each message for 2 seconds
    else:
        cyberpi.display.show_label("No Messages!", 16)

# Event handlers for button presses
@cyberpi.event.is_press('a')
def on_button_a_press():
    """Event handler for button A press."""
    send_message()

@cyberpi.event.is_press('b')
def on_button_b_press(): 
    """Event handler for button B press."""
    receive_messages()

# Main Program
connect_to_wifi()