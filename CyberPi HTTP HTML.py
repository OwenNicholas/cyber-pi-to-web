import network, socket
import event, time, cyberpi

ssid = 'Cyberspace'
password = '#bestinclass'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

cyberpi.display.show_label('Connected', 12, "top_mid", index= 0)
cyberpi.display.show_label(station.ifconfig(), 12, "center", index= 1)

def web_page():
  html = """
  <html>
  <head> <title>ESP Web Server</title> 
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> 
  <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}
  </style>
  </head>
  <body> 
    <h1>CyberPi Web Server</h1> 
    <h1>What do you want?</h1> 
  </body>
  </html>"""
  return html

while True:
  conn, addr = s.accept()
  
  cyberpi.display.show_label('Got a connection from %s' % str(addr), 12, "center", index= 1)
  request = conn.recv(1024)
  request = str(request)

  response = web_page()
  conn.sendall(response)
  conn.close()
  cyberpi.display.show_label('Connection Close by %s' % str(addr), 12, "center", index= 1)