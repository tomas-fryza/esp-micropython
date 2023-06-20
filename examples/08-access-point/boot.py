"""TBD.

TBD.

Inspired by:
    * https://www.engineersgarage.com/esp8266-esp32-based-wifi-access-point-using-micropython/
    * https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
"""

# Web server using sockets and Python socket API
try:
    import usocket as socket
except:
    import socket

import network

# Turn off vendor OS debugging messages
import esp
esp.osdebug(None)

# Run garbage collector to reclaim memory occupied by objects
# that are no longer used by the program
import gc
gc.collect()


def web_page():
    html = """<!DOCTYPE HTML><html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }
        h2 { font-size: 3.0rem; }
        p { font-size: 3.0rem; }
    </style>
</head>
<body>
    <h2>ESP32 Wi-Fi Access Point</h2>
    <p>Hello World!</p>
</body>
</html>"""
    return html


# Set Access Point name and password
SSID = "MicroPython-AP"
PSWD = "micro987654"

ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid=SSID, password=PSWD)

while not ap_if.active():
  pass

print("Connection successful")
print(ap_if.ifconfig())

# Create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print("Got a connection from %s" % str(addr))
  request = conn.recv(1024)
  print("Content = %s" % str(request))
  response = web_page()
  conn.send(response)
  conn.close()
