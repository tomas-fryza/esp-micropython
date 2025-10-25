"""
Wi-Fi configuration and connection

This MicroPython script configures and connects an ESP32
microcontroller to a Wi-Fi network. It display network-interface
and network-specific parameters.

Authors:
- Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
- Tomas Fryza

Creation date: 2023-06-16
Last modified: 2025-10-25
"""

import network
import wifi_utils
import config
import urequests  # Network Request Module

# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)

# Connect to SSID
wifi_utils.connect(wifi, config.SSID, config.PSWD)
# Get the current IP-level network-interface parameters
print("     IP               MASK            GATEWAY          DNS")
print(wifi.ifconfig())


# WRITE YOUR CODE HERE


# Get RSSI and network link Status
print()
print(wifi.status())
rssi = wifi.status("rssi")
print(f"Signal strength (RSSI): {rssi} dBm")


# Get Wi-Fi network-specific parameters
print()
prm = wifi.config("mac")
print("MAC address:", ':'.join([f"{b:02x}" for b in prm]))
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


print()
print("----- GET request -----")
url = "http://api.open-notify.org/iss-now.json"
response = urequests.get(url)

print("GET status code: ", end="")
print(response.status_code)
print("GET reason: ", end="")
print(response.reason)
print("GET text:")
print(response.text)
print("GET headers:")
print(response.headers)
# Close the response to free up resources
response.close()


print()
print("----- POST request -----")
url = "https://api.mathjs.org/v4/"
payload = {"expr": ["2+2", "sqrt(2)", "sin(pi/4)"]}
headers = {"Content-Type": "application/json"}
response = urequests.post(url, json=payload, headers=headers)

print("POST status code: ", end="")
print(response.status_code)
print("POST reason: ", end="")
print(response.reason)
print("POST text:")
print(response.text)
# print("POST headers:")
# print(response.headers)
response.close()


# Test if connected
print()
print(f"Is connected? {wifi.isconnected()}")
wifi_utils.disconnect(wifi)
print(f"Is connected? {wifi.isconnected()}")
