"""Scan Wi-Fi access points.

Activate the WLAN interface and scan for nearby access points (AP).
Display the main parameters of APs.

TODOs:
    * Add comments to all functions

Inspired by:
    * https://wokwi.com/projects/305570169692881473
    * https://github.com/micropython/micropython/issues/10017
"""

import network
import ubinascii  # Conversions between binary data and ASCII

# Create Station interface
sta_if = network.WLAN(network.STA_IF)
# Activate station/Wi-Fi client interface
sta_if.active(True)


def scan_wifi():
    print("Scanning for Wi-Fi networks, please wait... ", end="")

    # Perform a Wi-Fi APs scan
    accessPoints = sta_if.scan()

    print("Done")
    print("")

    print("SSID             | MAC               | Ch.| RSSI| AuthMode")
    print("-----------------+-------------------+----+-----+------------")

    authmodes = ["Open", "WEP", "WPA-PSK", "WPA2-PSK4",
                 "WPA/WPA2-PSK", "other", "other", "other"]

    # Print each AP params in a single row
    for (ssid, bssidap, channel, rssi, authmode, vis) in accessPoints:
        bssid = ubinascii.hexlify(bssidap, ":").decode()
        print(f"{ssid:16s} | {bssid:s} | {channel:2d} | {rssi:3d} | {authmodes[authmode]:s}")


# Call scanning function
scan_wifi()
