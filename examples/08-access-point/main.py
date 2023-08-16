"""Example of Wi-Fi access point.

Wi-Fi access point hosting a static webpage. Use a smartphon
to access web application.

Inspired by:
    * https://www.engineersgarage.com/esp8266-esp32-based-wifi-access-point-using-micropython/
    * https://www.engineersgarage.com/micropython-sockets-esp8266-esp32-tcp-server-tcp-client/
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
    """Static web page to be trasmited by AP

    :return:  HTML code to be displayed
    """
    html_code = """<!DOCTYPE HTML><html>
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
    return html_code


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
print("")

# Create TCP/IP socket object
# AF_INET == IPv4 internet protocols
# AF_INET6 == IPv6 internet protocols
# SOCK_STREAM == TCP type of socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to a port
# port number 80 == HTTP network service
s.bind(("", 80))
# Queue of 5 for incoming connections
s.listen(5)

while True:
    # Accept a new connection
    # conn: a new socket object that's used to transmit and receive data
    # address: IP address of the device
    conn, address = s.accept()
    print(f"Connection from {address} has been established.")

    # Receive data from the remote socket; maximum size is 512 bytes
    request = conn.recv(512)
    print(f"Request content ({len(request)} bytes):")
    print(request.decode())

    response = web_page()
    conn.send(response)
    conn.close()
