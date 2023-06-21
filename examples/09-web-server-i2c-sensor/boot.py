
"""Boot file of the web server for the DHT12 sensor data.

File contains the code that only needs to run once on boot and
imports libraries, network credentials, and connecting to your 
Wi-Fi network.

NOTES:
    * Set your Wi-Fi SSID and password

Inspired by:
    * https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
"""

# Web server using sockets and Python socket API
try:
    import usocket as socket
except:
    import socket

from machine import Pin, I2C
import network
from time import sleep_ms

# Turn off vendor OS debugging messages
import esp
esp.osdebug(None)

# Run garbage collector to reclaim memory occupied by objects
# that are no longer used by the program
import gc
gc.collect()

# Network settings
# WIFI_SSID = "<YOUR WIFI SSID>"
# WIFI_PSWD = "<YOUR WIFI PASSWORD>"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    print("Connecting to Wi-Fi", end="")

    # Activate station/Wi-Fi client interface and connect
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PSWD)

    # Wait untill the connection is estalished
    while not sta_if.isconnected():
        print(".", end="")
        sleep_ms(100)

    print("Connected")
    print(f"Network config: {sta_if.ifconfig()}")
