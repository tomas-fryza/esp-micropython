"""
Wi-Fi network scanner

This MicroPython script scans for available Wi-Fi networks
using the ESP32's Wi-Fi interface in Station mode. It prints
the RSSI (Received Signal Strength Indicator), channel, and
SSID (Service Set Identifier) of each detected network.

Authors:
- Wokwi
- Tomas Fryza

Creation date: 2023-06-16
Last modified: 2026-05-07
"""

# MicroPython builtin modules
import network
import time

# Initialize the Wi-Fi interface in Station mode and activate it
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

try:
    while True:
        print()
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

        time.sleep(5)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
    wifi.active(False)
