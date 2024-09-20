"""
MicroPython Wi-Fi access point scanner

This MicroPython script scans for nearby Wi-Fi access points
(APs) using an ESP32 microcontroller and displays their SSID
(Service Set Identifier, aka network's name), channel index,
and signal strength (RSSI).

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Run the script
2. Wait for results

Author: Wokwi, Tomas Fryza
Date: 2023-09-21
"""

import network
from machine import Pin

status_led = Pin(2, Pin.OUT)

# Initialize the Wi-Fi interface in Station mode and activate it
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Perform the Wi-Fi scan
status_led.on()
print("Scanning Wi-Fi... ", end="")
nets = wifi.scan()
print(f"{len(nets)} network(s)")
status_led.off()

# print(nets[0])

# Print the list of available Wi-Fi networks
print("RSSI Channel \tSSID")
for net in nets:
    rssi = net[3]
    channel = net[2]
    ssid = net[0].decode("utf-8")
    print(f"{rssi}  (ch.{channel}) \t{ssid}")
