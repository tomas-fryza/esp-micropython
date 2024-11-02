"""
Wi-Fi network scanner
=====================

This MicroPython script scans for available Wi-Fi networks
using the ESP32's Wi-Fi interface in Station mode. It prints
the RSSI (Received Signal Strength Indicator), channel, and
SSID (Service Set Identifier) of each detected network.

Components:
- ESP32-based board

Authors:
- Wokwi
- Tomas Fryza

Creation date: 2023-06-16
Last modified: 2024-11-02
"""

import network

# Initialize the Wi-Fi interface in Station mode and activate it
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Perform the Wi-Fi scan
print("Scanning Wi-Fi networks... ", end="")
nets = wifi.scan()
print(f"{len(nets)} network(s) found.")

# Print the list of available Wi-Fi networks
print("RSSI\tChannel\tSSID")
for net in nets:
    rssi = net[3]  # Signal strength
    channel = net[2]  # Channel number
    ssid = net[0].decode("utf-8")  # SSID (network name)
    print(f"{rssi}\t(ch.{channel})\t{ssid}")
