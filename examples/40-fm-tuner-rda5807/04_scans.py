"""
MicroPython demo for ESP32: Wi-Fi scanner with OLED display

This script initializes the OLED display (SSD1306) and continuously scans 
for the strongest Wi-Fi network.

Requires: SSD1306 OLED library, I2C connectivity

Author:
- Tomas Fryza

Creation date: 2025-04-28
Last modified: 2025-05-18

Inspired by:
  * https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
"""

# MicroPython builtin modules
from machine import Pin
from machine import SoftI2C
import time
import network

# External modules
import ssd1306  # OLED display


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.contrast(100)
    display.fill(0)
    return display


def i2c_scan(display):
    print("Scanning I2C... ", end="")
    display.text("Scanning I2C...", 0, 5)

    addrs = i2c.scan()
    # Scanning I2C... 5 device(s) detected
    # dec. hex.
    # 16   0x10 -- rda5807 (sequential access / RDA5800 mode)
    # 17   0x11 -- rda5807 (random access / RDA5807 mode)
    # 60   0x3c -- OLED
    # 96   0x60 -- rda5807 (TEA5767 compatible mode)
    # 119  0x77 -- bmp180 (pressure/temperature)
    print(f"{len(addrs)} device(s) detected")

    print("dec.\t hex.")
    y = 16
    for addr in addrs:
        print(f"{addr}\t {hex(addr)}")
        display.text(hex(addr), 0, y)
        y += 8
    display.show()  # Write the contents of the FrameBuffer to display memory


def show_logo(display):
    """
    Draw logo (VUT Brno stylized)
    https://www.designportal.cz/clanky/aktualizovano-vut-v-brne-bude-mit-nove-logo/
    """
    # x, y, width, height, color
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(5, 5, 10, 4, 0)
    display.fill_rect(15, 9, 12, 3, 0)
    display.fill_rect(15, 12, 4, 15, 0)
    # x, y, color
    display.pixel(19, 12, 0)
    # string, x, y
    display.text("STEAM jcmm", 35, 5)
    display.text("VUT Brno", 35, 16)
    display.text("Radioelektr.", 35, 24)
    display.show()


def init_wifi():
    """Initialize WLAN interface."""
    # Create a WLAN object (for STA mode, i.e., station/client mode)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # Activate the interface if it's not already
    return wlan


def show_wifi(display, ssid, rssi):
    """Display SSID and RSSI on the screen."""
    display.fill_rect(0, 48, 128, 16, 0)  # Clear only lower portion
    display.text(f"{ssid[:16]}", 0, 48)
    display.text(f"{rssi} dBm", 0, 56)
    display.show()


i2c = SoftI2C(sda=Pin(21), scl=Pin(22))

display = init_display(i2c)
i2c_scan(display)
time.sleep(5)
display.fill(0)

# Display invert animation
show_logo(display)
for _ in range(3):
    display.invert(1)
    time.sleep(0.5)
    display.invert(0)
    time.sleep(0.5)

wlan = init_wifi()

# Optional: Show MAC address
# mac_bytes = wlan.config('mac')
# mac_str = ':'.join(f'{b:02x}' for b in mac_bytes)

# display.text("MAC:", 0, 38)
# display.text(f"{mac_str}", 0, 48)
# display.show()
# print(f"ESP32 MAC address: {mac_str}")
# time.sleep(5)

display.text("Strongest Wi-Fi:", 0, 38)
print("Scanning for Wi-Fi networks... Press Ctrl+C to stop.")

try:
    # Forever loop
    while True:
        networks = wlan.scan()
        if networks:
            # Each network is: (ssid, bssid, channel, RSSI, authmode, hidden)
            ssid = networks[0][0].decode("utf-8")
            rssi = networks[0][3]

            show_wifi(display, ssid, rssi)
            print(f"Strongest: {ssid} ({rssi} dBm)")
        else:
            show_wifi(display, "<no networks>", 0)
            print("No networks found")
        time.sleep(1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    display.poweroff()
    wlan.active(False)
