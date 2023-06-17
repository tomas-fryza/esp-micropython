"""Connect to a Wi-Fi network.

Use `network` module to establish the connection to the Wi-Fi
network.

See also:
    https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
    https://docs.micropython.org/en/latest/esp32/quickref.html
"""

import network

wlan_sta = network.WLAN(network.STA_IF)


def connect(ssid, pswd):
    print("Connecting...")

    if wlan_sta.isconnected() == True:
        print("Already connected")
        return

    wlan_sta.active(True)
    wlan_sta.connect(ssid, pswd)

    while wlan_sta.isconnected() == False:
        pass

    print("Connection successful")
    # Get the interface's IP/netmask/gw/DNS addresses
    # Note that, the IP assigned to the ESP32 is local,
    # so we can not use it to receive connections from outside
    # your network without portforwarding the router
    print(wlan_sta.ifconfig())


def disconnect():
    if wlan_sta.active() == True:   
        wlan_sta.active(False)

    if wlan_sta.isconnected() == False:
        print("Disconnected")


connect("your-ssid", "your-password")
disconnect()
