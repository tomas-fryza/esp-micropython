"""
This module provides functions for connecting to and
disconnecting from a Wi-Fi network using MicroPython on
ESP8266 or ESP32 devices.

Example
-------
.. code-block:: python

    from wifi_module import connect, disconnect

    # Initialize the Wi-Fi interface in Station mode
    wifi = network.WLAN(network.STA_IF)

    # Connect to Wi-Fi
    if connect(wifi, "Your_SSID", "Your_Password"):
        print("Connected to Wi-Fi!")
    else:
        print("Failed to connect.")

    # Disconnect from Wi-Fi
    disconnect(wifi)
    print("Disconnected from Wi-Fi.")

Authors
-------
- Nikhil Agnihotri, `Engineers Garage <https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/>`_
- Tomas Fryza

Modification history
--------------------
- **2024-12-14** : Prefixes added to print statements.
- **2024-11-11** : Added Sphinx comments.
- **2024-11-02** : Added `print_status` method.
- **2023-06-17** : Created `connect` and `disconnect` methods.
"""

import time
import gc  # Garbage Collector interface (Memory management)
gc.collect()

print_info = False


def connect(wifi, ssid, password):
    """
    Connect to a specified Wi-Fi network using the provided
    SSID and password. If the connection attempt exceeds the
    specified timeout, it will terminate and return `False`.
    
    :param wifi: The Wi-Fi interface object to use for the connection.
    :param str ssid: The SSID of the Wi-Fi network to connect to.
    :param str password: The password for the Wi-Fi network.
    :returns: `True` if connected successfully, `False` if
              the connection attempt timed out.
    """

    if not wifi.isconnected():
        wifi.active(True)
        print(f"[wifi] Connecting to {ssid}...", end="")
        wifi.connect(ssid, password)

        for _ in range(40):
            if wifi.isconnected():
                print(" Done")
                return True
            else:
                if print_info:
                    print_status(wifi)
                else:
                    print(".", end="")
                time.sleep_ms(250)

        print("\r\n\x1b[31m[wifi] Connection failed\x1b[0m")
        wifi.disconnect()
        return False
    else:
        print("[wifi] Already connected")
        if print_info:
            print_status(wifi)
    return True


def disconnect(wifi):
    """
    Deactivates the specified Wi-Fi interface and checks if
    the device is not connected to any Wi-Fi network.

    :param wifi: The Wi-Fi interface object to disconnect.
    """
    if wifi.active():
        wifi.active(False)

    if not wifi.isconnected():
        print("[wifi] Deactivated/disconnected")

    if print_info:
        print_status(wifi)


def print_status(wifi):
    """
    Retrieves the status of the specified Wi-Fi interface and
    prints a human-readable message corresponding to that status.

    :param wifi: The Wi-Fi interface object whose status is to
                 be printed.
    """
    status = wifi.status()
    print(f"[wifi] {status_messages.get(status)}")


status_messages = {
    1000: "STAT_IDLE -- 1000",
    1001: "STAT_CONNECTING -- 1001",
    1010: "STAT_GOT_IP -- 1010",
    200: "STAT_BEACON_TIMEOUT -- 200",
    201: "STAT_NO_AP_FOUND -- 201",
    202: "STAT_WRONG_PASSWORD -- 202",
    203: "STAT_ASSOC_FAIL -- 203",
    204: "STAT_HANDSHAKE_TIMEOUT -- 204"
}
