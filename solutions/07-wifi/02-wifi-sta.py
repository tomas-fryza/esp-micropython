"""
Wi-Fi configuration and connection
==================================

This MicroPython script configures and connects an ESP32
microcontroller to a Wi-Fi network. It display network-interface
and network-specific parameters.

Components:
- ESP32 microcontroller

Authors:
- Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
- Tomas Fryza

Creation Date:
- 2023-06-16

Last Modified:
- 2024-11-02
"""

import network
import my_wifi
import config
import urequests  # Network Request Module

# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)

# Connect to SSID
my_wifi.connect(wifi, config.SSID, config.PSWD)
# Get the current IP-level network-interface parameters
print("     IP               MASK            GATEWAY          DNS")
print(wifi.ifconfig())


# WRITE YOUR CODE HERE


# Get Wi-Fi network-specific parameters
print("")
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

# Get RSSI and network link Status
print("")
rssi = wifi.status("rssi")
print(f"Signal strength (RSSI): {rssi} dBm")
print(wifi.status())

print("Make the GET request")
response = urequests.get("https://catfact.ninja/fact")
print(response.status_code)
print(response.reason)
print(response.text)
print(response.headers)
# Close the response to free up resources
response.close()

print("Make the POST request")
json = {"fromTimeZone": "Europe/Prague",
       "dateTime": "2024-10-26 15:33:00",
       "toTimeZone": "America/Los_Angeles",
       "dstAmbiguity": ""}
headers = {"Content-Type": "application/json"}
response = urequests.post("https://timeapi.io/api/conversion/converttimezone",
                          json=json,
                          headers=headers)
print(response.status_code)
print(response.reason)
print(response.text)
print(response.headers)
response.close()

# Test if connected
print("")
print(f"Is connected? {wifi.isconnected()}")
my_wifi.disconnect(wifi)
print(f"Is connected? {wifi.isconnected()}")
