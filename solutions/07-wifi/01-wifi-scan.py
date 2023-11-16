"""
Wi-Fi Network Scanner

This MicroPython script scans for available Wi-Fi networks using
the ESP32's Wi-Fi interface in Station mode. It prints the RSSI
(Received Signal Strength Indicator), channel, and SSID (Service
Set Identifier) of each detected network.

Authors: Wokwi, Tomas Fryza
Date: 2023-06-16
"""

import network

# Initialize the Wi-Fi interface in Station mode and activate it
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Perform the Wi-Fi scan
print("Scanning for Wi-Fi... ", end="")
nets = wifi.scan()
print(f"{len(nets)} network(s)")

# Print the list of available Wi-Fi networks
print("RSSI Channel \tSSID")
for net in nets:
    rssi = net[3]
    channel = net[2]
    ssid = net[0].decode("utf-8")
    print(f"{rssi}  (ch.{channel}) \t{ssid}")
