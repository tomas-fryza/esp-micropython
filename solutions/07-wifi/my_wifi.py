"""
Wi-Fi Connection Management for MicroPython

This module provides functions to connect and disconnect
from a Wi-Fi network.

Components:
  - ESP32 microcontroller

Authors: Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
         Tomas Fryza
Creation Date: 2023-06-17
Last Modified: 2024-10-25
"""

import gc  # Garbage Collector interface (Memory management)
gc.collect()


def connect(wifi, ssid, password, timeout=10):
    """
    Connect to Wi-Fi network.

    Activates the Wi-Fi interface, connects to the specified network,
    and waits until timeout or the connection is established.

    :return: None
    """
    import time

    if not wifi.isconnected():
        wifi.active(True)
        wifi.connect(ssid, password)

        start_time = time.time()

        symbols = ["/", "-", "\\", "|"]
        i = 0
        while not wifi.isconnected():
            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                print("Connection attempt timed out.")
                return False
    
            print(f"Connecting to {ssid}... {symbols[i]}", end="\r")
            time.sleep(0.1)
            i = (i + 1) % 4
        print(f"Connecting to {ssid}... Done")
    else:
        print("Already connected")


def disconnect(wifi):
    """
    Disconnect from Wi-Fi network.

    Deactivates the Wi-Fi interface if active and checks if
    the device is not connected to any Wi-Fi network.

    :return: None
    """
    if wifi.active():
        wifi.active(False)

    if not wifi.isconnected():
        print("Disconnected")
