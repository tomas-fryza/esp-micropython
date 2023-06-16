"""Scan Wi-Fi access points.

Activate the WLAN interface and scan for nearby access points (AP).
Display the main parameters of APs.

See also:
    https://wokwi.com/projects/305570169692881473
    https://github.com/micropython/micropython/issues/10017
"""

import network
import ubinascii

# Initialize wlan object
wlan = network.WLAN(network.STA_IF)
# Activate wlan interface
wlan.active(True)


def scan():
    print("Scanning for Wi-Fi networks, please wait...", end="")

    # Perform a Wi-Fi APs scan
    accessPoints = wlan.scan()

    print("Done")
    print("")

    print("SSID             | MAC               | Ch.| RSSI| AuthMode")
    print("-----------------+-------------------+----+-----+------------")

    authmodes = ["Open", "WEP", "WPA-PSK", "WPA2-PSK4", "WPA/WPA2-PSK", "other"]

    # Print each AP found in a single row
    for (ssid, bssidap, channel, rssi, authmode, vis) in accessPoints:
        bssid =  ubinascii.hexlify(bssidap,":").decode()
        print(f"{ssid:16s} | {bssid:s} | {channel:2d} | {rssi:3d} | {authmodes[authmode]:s}")

# Call scanning function
scan()
