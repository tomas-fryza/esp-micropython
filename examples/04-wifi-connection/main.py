"""Connect to a Wi-Fi network.

Use `network` module to establish the connection to the Wi-Fi
network.

See also:
    https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
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
    print(wlan_sta.ifconfig())
    # Note that the IP assigned to the ESP32 is local,
    # so we can not use it to receive connections from outside
    # your network without portforwarding the router


def disconnect():
    if wlan_sta.active() == True:   
        wlan_sta.active(False)

    if wlan_sta.isconnected() == False:
        print("Disconnected")


connect("your-ssid", "your-password")
disconnect()
