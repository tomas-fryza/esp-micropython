"""Scan Wi-Fi access points.

Activate the WLAN interface and scan for nearby access points (AP).
Display SSID, channel index and signal strength of APs.

Inspired by:
    * https://wokwi.com/projects/305570169692881473
    * https://github.com/micropython/micropython/issues/10017
"""

import network

# Initialize the WLAN (Station mode interface)
sta_if = network.WLAN(network.STA_IF)
# Activate station/Wi-Fi client interface
sta_if.active(True)

# Perform the Wi-Fi APs scan
print("Scanning for Wi-Fi networks, please wait... ", end="")
available_networks = sta_if.scan()
print("Done")
print("")

# Print the list of available Wi-Fi networks
print("SSID              | Channel | Signal Strength (dBm)")
print("------------------+---------+----------------------")
for network in available_networks:
    print(f"{network[0].decode("utf-8"):17s} | {network[2]:7d} | {network[3]:10d}")
