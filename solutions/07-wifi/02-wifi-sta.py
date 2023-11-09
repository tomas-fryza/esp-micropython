"""
ESP32 Wi-Fi Configuration and Connection

This MicroPython script configures and connects an ESP32 microcontroller
to a Wi-Fi network. It includes functions to connect, disconnect,
and display Wi-Fi configuration details.

Usage:
1. Update the `WIFI_SSID` and `WIFI_PSWD` with your Wi-Fi credentials.
2. Upload and run the script on your ESP32 device.

Authors: Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
         Tomas Fryza
Date: 2023-06-16
"""
import network

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"

# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)


def connect_wifi():
    """
    Connect to Wi-Fi network.

    Activates the Wi-Fi interface, connects to the specified network,
    and waits until the connection is established.

    :return: None
    """
    from time import sleep_ms

    if not wifi.isconnected():
        print(f"Connecting to `{WIFI_SSID}`", end="")

        # Activate the Wi-Fi interface
        wifi.active(True)

        # Connect to the specified Wi-Fi network
        wifi.connect(WIFI_SSID, WIFI_PSWD)

        # Wait untill the connection is estalished
        while not wifi.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")
    else:
        print("Already connected")


def disconnect_wifi():
    """
    Disconnect from Wi-Fi network.

    Deactivates the Wi-Fi interface if active and checks if
    the device is not connected to any Wi-Fi network.

    :return: None
    """
    # Check if the Wi-Fi interface is active
    if wifi.active():
        # Deactivate the Wi-Fi interface
        wifi.active(False)

    # Check if the device is not connected to any Wi-Fi network
    if not wifi.isconnected():
        print("Disconnected")



connect_wifi()

# Get the current IP configuration of the interface
config = wifi.ifconfig()

# Print the configuration
print("Wi-Fi Configuration:")
print(f"IP address: \t{config[0]}")
print(f"Subnet mask:\t{config[1]}")
print(f"Gateway: \t{config[2]}")
print(f"DNS server:\t{config[3]}")

rssi = wifi.status("rssi")
print("Signal strength (RSSI):", rssi)

mac_address = wifi.config('mac')
print("MAC address:", ':'.join(['{:02x}'.format(b) for b in mac_address]))

is_connected = wifi.isconnected()
print("Is connected:", is_connected)

disconnect_wifi()

is_connected = wifi.isconnected()
print("Is connected:", is_connected)
