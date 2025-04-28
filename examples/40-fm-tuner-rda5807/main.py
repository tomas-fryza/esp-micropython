"""
MicroPython demo for ESP32: Wi-Fi scanner with OLED display

This script initializes the OLED display (SSD1306) and continuously scans 
for the strongest Wi-Fi network.

Requires: SSD1306 OLED library, I2C connectivity

Author:
- Tomas Fryza

Creation date: 2025-04-28
Last modified: 2025-04-28

Inspired by:
  * https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
"""

# MicroPython builtin modules
import time
from machine import Pin, SoftI2C
import network
import esp
esp.osdebug(None)  # Optional: disable debug output

# External modules
import ssd1306  # OLED display

# Constants
I2C_SDA = 21
I2C_SCL = 22
LED_PIN = 2

def init_display():
    """Initialize the OLED display and show startup screen."""
    i2c = SoftI2C(sda=Pin(21), scl=Pin(22))  #, freq=400_000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.sleep(False)
    display.contrast(100)
    display.fill(0)

    # Draw logo (VUT Brno stylized)
    # https://www.designportal.cz/clanky/aktualizovano-vut-v-brne-bude-mit-nove-logo/
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(5, 5, 14, 8, 0)
    display.fill_rect(15, 9, 26, 11, 0)
    display.fill_rect(15, 12, 18, 26, 0)
    display.pixel(19, 12, 0)

    display.text("STEAM jcmm", 40, 0)
    display.text("VUT Brno", 40, 12)
    display.text("RadioElect.", 40, 24)
    display.show()  # Write the contents of the FrameBuffer to display memory
    return display

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

def main():
    led = Pin(LED_PIN, Pin.OUT)
    led.off()

    display = init_display()
    wlan = init_wifi()

    # Initial LED blink and display invert animation
    for _ in range(3):
        led.on()
        display.invert(1)
        time.sleep(0.5)
        led.off()
        display.invert(0)
        time.sleep(0.5)

    # Optional: Show MAC address
    # mac_bytes = wlan.config('mac')
    # mac_str = ':'.join(f'{b:02x}' for b in mac_bytes)

    # display.text("MAC:", 0, 40)
    # display.text(f"{mac_str}", 0, 48)
    # display.show()

    display.text("Strongest WiFi:", 0, 40)
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
            time.sleep(2)

    except KeyboardInterrupt:
        # This part runs when Ctrl+C is pressed
        print("Program interrupted. Cleaning up...")

        # Optional cleanup code
        display.poweroff()
        led.off()
        wlan.active(False)

# Only run if not imported
if __name__ == "__main__":
    main()
