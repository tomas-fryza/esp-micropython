# https://docs.micropython.org/en/latest/library/network.WLAN.html

import network

# Initialize the Wi-Fi interface in Station (client) mode
wifi = network.WLAN(network.STA_IF)
# Activate the interface
wifi.active(True)

# Perform the Wi-Fi APs scan
print("Scanning for Wi-Fi... ", end="")
available_networks = wifi.scan()
print(f"{len(available_networks)} networks")

# Print the list of available Wi-Fi networks
for net in available_networks:
    ssid = net[0].decode("utf-8")
    channel = net[2]
    rssi = net[3]
    print(f"{rssi} (ch. {channel})\t{ssid}")
