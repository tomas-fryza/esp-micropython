"""
MicroPython demo for ESP32: Wi-Fi scanner with OLED display

This script initializes the OLED display and continuously
scans for the strongest Wi-Fi network.

Requires: SH1106 or SSD1306 OLED library, I2C connectivity

Author:
- Tomas Fryza

Creation date: 2025-04-28
Last modified: 2026-05-07

Inspired by:
  * https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
"""

# MicroPython builtin modules
from machine import Pin
from machine import I2C
import time
import network

# External modules
from sh1106 import SH1106_I2C
# from ssd1306 import SSD1306_I2C


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    display = SH1106_I2C(i2c)
    # display = SSD1306_I2C(128, 64, i2c)
    display.contrast(100)
    display.fill(0)
    return display


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
    display.text("TechDay", 35, 5)
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


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
print(f"I2C configuration : {str(i2c)}")

display = init_display(i2c)
display.fill(0)
show_logo(display)

led = Pin(2, Pin.OUT)
wlan = init_wifi()

display.text("Strongest Wi-Fi:", 0, 38)
print("Scanning for Wi-Fi networks every 5 secs.")
print()
print("Press Ctrl+C to stop.")
print()

try:
    while True:
        led.on()
        networks = wlan.scan()
        if networks:
            # Each network is: (ssid, bssid, channel, RSSI, authmode, hidden)
            ssid = networks[0][0].decode("utf-8")
            rssi = networks[0][3]

            show_wifi(display, ssid, rssi)
            print(f"Strongest Wi-Fi: {ssid} ({rssi} dBm)")
        else:
            show_wifi(display, "<no networks>", 0)
            print("No networks found")
        led.off()
        time.sleep(5)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")

    # Optional cleanup code
    display.poweroff()
    led.off()
    wlan.active(False)
