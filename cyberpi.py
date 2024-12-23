import cyberpi
import websocket
import json
import time
import threading

# Constants for Wi-Fi and WebSocket URL
WIFI_SSID = "Cyberspace"
WIFI_PASSWORD = "#bestinclass"
WS_URL = "ws://192.168.18.244:8080/ws"  # Replace with your Ktor WebSocket server URL

# Global variable to store WebSocket connection and messages
ws = None
messages = []


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


def on_message(ws, message):
    """Callback for receiving WebSocket messages."""
    global messages
    try:
        # Parse incoming messages
        received = json.loads(message)
        if isinstance(received, list):
            messages = received  # For multiple messages
        else:
            messages.append(received)  # For a single message
        cyberpi.display.clear()
        cyberpi.display.show_label("Msg Received!", 16)
        print(f"Received: {received}")
    except Exception as e:
        print(f"Error processing message: {e}")


def on_error(ws, error):
    """Callback for WebSocket errors."""
    print(f"WebSocket Error: {error}")
    cyberpi.display.show_label("WS Error!", 16)


def on_close(ws, close_status_code, close_msg):
    """Callback for WebSocket connection closing."""
    print("WebSocket Closed")
    cyberpi.display.show_label("WS Closed!", 16)


def on_open(ws):
    """Callback for WebSocket connection opening."""
    print("WebSocket Connected")
    cyberpi.display.show_label("WS Connected", 16)
    ws.send(json.dumps({"content": "Hello from CyberPi!"}))  # Initial message


def start_websocket():
    """Start the WebSocket client."""
    global ws
    cyberpi.display.show_label("Connecting WS...", 16)
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    # Run WebSocket client in a separate thread to avoid blocking CyberPi's main loop
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()


def send_message():
    """Send a message through the WebSocket."""
    global ws
    message = {"content": "Halo bro from CyberPi!"}
    if ws:
        try:
            ws.send(json.dumps(message))
            cyberpi.display.show_label("Msg Sent!", 16)
        except Exception as e:
            print(f"Error sending message: {e}")
            cyberpi.display.show_label("Send Error!", 16)
    else:
        cyberpi.display.show_label("No WS Connection", 16)


def show_received_messages():
    """Display received messages."""
    global messages
    cyberpi.display.clear()
    if messages:
        for msg in messages[-5:]:  # Display the last 5 messages
            content = msg.get("content", "No content")
            cyberpi.display.show_label(content, 16)
            time.sleep(2)  # Show each message for 2 seconds
    else:
        cyberpi.display.show_label("No Messages!", 16)


# Event handlers for button presses
@cyberpi.event.is_press("a")
def on_button_a_press():
    """Send a message when button A is pressed."""
    send_message()


@cyberpi.event.is_press("b")
def on_button_b_press():
    """Show received messages when button B is pressed."""
    show_received_messages()


# Main Program
connect_to_wifi()
start_websocket()
while True:
    # Keep the program alive
    time.sleep(1)