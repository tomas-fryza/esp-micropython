"""Connect to a Wi-Fi network.

Use `network` module to establish the connection to the Wi-Fi
network.

TODOs:
    * Add comments to all functions

Inspired by:
    * https://www.srccodes.com/configuration-sta-if-interface-esp8266-mycro-python-firmware-connect-wifi-networkk-automatically-boot/
    * https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
    * https://docs.micropython.org/en/latest/esp32/quickref.html
"""

import network


def connect_wifi():
    from time import sleep_ms
    import ubinascii

    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")

        # Activate station/Wi-Fi client interface
        sta_if.active(True)

        # Connect
        sta_if.connect(WIFI_SSID, WIFI_PSWD)

        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")

    else:
        print("Already connected")

    # Get the interface's IP/netmask/gw/DNS addresses
    # Note that, the IP assigned to the ESP32 is local,
    # so we can not use it to receive connections from outside
    # your network without portforwarding the router
    print(f"Network config: {sta_if.ifconfig()}")

    # Get MAC address
    macAddr = network.WLAN().config("mac")

    # Convert binary to ASCII
    binaryToAscii = ubinascii.hexlify(macAddr, ":")
    print(f"MAC: {macAddr} --> {binaryToAscii} --> {binaryToAscii.decode()}")


def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

connect_wifi()
disconnect_wifi()
