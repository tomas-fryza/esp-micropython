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
Last Modified: 2024-10-25
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
params = wifi.ifconfig()
print("")
print(f"IP address: \t{params[0]}")
print(f"Subnet mask:\t{params[1]}")
print(f"Gateway: \t{params[2]}")
print(f"DNS server:\t{params[3]}")

# Get Wi-Fi network-specific parameters
print("")
param = wifi.config("mac")
print("MAC address:", ':'.join(['{:02x}'.format(b) for b in param]))
param = wifi.config("ssid")
print(f"Wi-Fi access point name: {param}")
param = wifi.config("channel")
print(f"Wi-Fi channel: {param}")
param = wifi.config("hostname")
print(f"Host name: {param}")
param = wifi.config("reconnects")
print(f"Number of reconnect attemps: {param}")
param = wifi.config("txpower")
print(f"Maximum transmit power: {param} dBm")

# Get RSSI
print("")
rssi = wifi.status("rssi")
print(f"Signal strength (RSSI): {rssi} dBm")

# Test if connected
print("")
is_connected = wifi.isconnected()
print(f"Is connected: {is_connected}")

my_wifi.disconnect(wifi)

is_connected = wifi.isconnected()
print(f"Is connected: {is_connected}")
