"""
ESP32 Wi-Fi Configuration and Connection

This MicroPython script configures and connects an ESP32 microcontroller
to a Wi-Fi network. It includes functions to connect, disconnect,
and display network-interface and network-specific parameters.

Components:
  - ESP32 microcontroller

Authors: Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
         Tomas Fryza
Creation Date: 2023-06-16
Last Modified: 2024-10-26
"""

import network
import my_wifi
import config

# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)

# Connect to SSID
my_wifi.connect(wifi, config.SSID, config.PSWD)


# WRITE YOUR CODE HERE


# Get the current IP-level network-interface parameters
prms = wifi.ifconfig()
print("")
print(f"IP address: \t{prms[0]}")
print(f"Subnet mask:\t{prms[1]}")
print(f"Gateway: \t{prms[2]}")
print(f"DNS server:\t{prms[3]}")

# Get Wi-Fi network-specific parameters
print("")
prm = wifi.config("mac")
print("MAC address:", ':'.join(['{:02x}'.format(b) for b in prm]))
prm = wifi.config("ssid")
print(f"Wi-Fi access point name: {prm}")
prm = wifi.config("channel")
print(f"Wi-Fi channel: {prm}")
prm = wifi.config("hostname")
print(f"Host name: {prm}")
prm = wifi.config("reconnects")
print(f"Number of reconnect attemps: {prm}")
prm = wifi.config("txpower")
print(f"Maximum transmit power: {prm} dBm")

# Get RSSI and network link Status
print("")
rssi = wifi.status("rssi")
print(f"Signal strength (RSSI): {rssi} dBm")
print(wifi.status())

# Test if connected
print("")
print(f"Is connected? {wifi.isconnected()}")
my_wifi.disconnect(wifi)
print(f"Is connected? {wifi.isconnected()}")
