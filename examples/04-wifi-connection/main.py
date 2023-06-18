"""Connect to a Wi-Fi network.

Use `network` module to establish the connection to the Wi-Fi
network.

See also:
    https://www.srccodes.com/configuration-sta-if-interface-esp8266-mycro-python-firmware-connect-wifi-networkk-automatically-boot/
    https://www.engineersgarage.com/micropython-wifi-network-esp8266-esp32/
    https://docs.micropython.org/en/latest/esp32/quickref.html
"""

import network


def connect():
    from time import sleep_ms
    import ubinascii

    if not sta_if.isconnected():
        print("Connecting to network...")

        # Activate station/Wi-Fi client interface
        sta_if.active(True)

        # Connect
        sta_if.connect(YOUR_WIFI_SSID, YOUR_WIFI_PSWD)

        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            sleep_ms(250)

        print("Connection successful")

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


def disconnect():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


YOUR_WIFI_SSID = "ssid"
YOUR_WIFI_PSWD = "pswd"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

connect()
# disconnect()
