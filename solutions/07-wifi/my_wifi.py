"""
Wi-Fi Connection Management for MicroPython

This module provides functions to connect and disconnect
from a Wi-Fi network.

Components:
  - ESP32 microcontroller

Authors: Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
         Tomas Fryza
Creation Date: 2023-06-17
Last Modified: 2024-10-26
"""

import gc  # Garbage Collector interface (Memory management)
gc.collect()

print_info = False


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
        print(f"Connecting to {ssid} (timeout {timeout} sec)...", end="")

        start_time = time.time()

        while not wifi.isconnected():
            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                print("Connection attempt timed out.")
                return False

            time.sleep(0.25)
            if print_info:
                print_status(wifi)
            else:
                print(".", end="")
        print(" Done")
    else:
        print("Already connected")
        if print_info:
            print_status(wifi)


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

    if print_info:
        print_status(wifi)


def print_status(wifi):
    status = wifi.status()
    print(f"[WIFI] {status_messages.get(status)}")


status_messages = {
    1000: "STAT_IDLE -- 1000",
    1001: "STAT_CONNECTING -- 1001",
    1010: "STAT_GOT_IP -- 1010",
    201: "STAT_NO_AP_FOUND -- 201",
    202: "STAT_WRONG_PASSWORD -- 202",
    200: "STAT_BEACON_TIMEOUT -- 200",
    203: "STAT_ASSOC_FAIL -- 203",
    204: "STAT_HANDSHAKE_TIMEOUT -- 204"
}
