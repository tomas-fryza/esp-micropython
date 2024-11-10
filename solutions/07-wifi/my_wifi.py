"""
Wi-Fi connection management

This module provides functions to connect and disconnect
from a Wi-Fi network.

Authors:
- Nikhil Agnihotri, https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
- Tomas Fryza

Creation date: 2023-06-17
Last modified: 2024-11-02
"""

import gc  # Garbage Collector interface (Memory management)
gc.collect()

print_info = False


def connect(wifi, ssid, password, timeout=10):
    """
    Connect to a Wi-Fi network.

    This function attempts to connect to a specified Wi-Fi
    network using the provided SSID and password. If the
    connection attempt exceeds the specified timeout, it
    will terminate and return `False`.
    
    :param wifi: The Wi-Fi interface object to use for the connection.
    :type wifi: network.WLAN
    :param str ssid: The SSID of the Wi-Fi network to connect to.
    :param str password: The password for the Wi-Fi network.
    :param int timeout: The maximum time in seconds to wait
                        for the connection attempt.
    :returns: `True` if connected successfully, `False` if
              the connection attempt timed out.
    :rtype: bool
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
    return True


def disconnect(wifi):
    """
    Disconnect from the Wi-Fi network.

    This function deactivates the specified Wi-Fi interface
    and checks if the device is not connected to any Wi-Fi
    network.

    :param wifi: The Wi-Fi interface object to disconnect.
    :type wifi: network.WLAN
    """
    if wifi.active():
        wifi.active(False)

    if not wifi.isconnected():
        print("Disconnected")

    if print_info:
        print_status(wifi)


def print_status(wifi):
    """
    Print the current status of the Wi-Fi connection.

    This function retrieves the status of the specified
    Wi-Fi interface and prints a human-readable message
    corresponding to that status.

    :param wifi: The Wi-Fi interface object whose status
                 is to be printed.
    :type wifi: network.WLAN
    """
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
