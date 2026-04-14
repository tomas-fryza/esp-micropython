"""
OLED drawing functions

Example of basic OLED drawing functions, via FrameBuffer.
These functions are available directly from the ssd1306
OLED object since it inherits from framebuf.FrameBuffer.

Requires: SSD1306 OLED library, I2C connectivity

Author:
- Tomas Fryza

Creation date: 2025-05-18
Last modified: 2025-05-18
"""

# MicroPython builtin modules
from machine import Pin
from machine import SoftI2C, I2C
import time

# External modules
# import ssd1306  # OLED display
from sh1106 import SH1106_I2C


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    # display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display = SH1106_I2C(i2c)
    display.contrast(100)
    display.fill(0)
    return display


# i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
print(f"I2C configuration : {str(i2c)}")

display = init_display(i2c)

# string, x, y
display.text("STEAM jcmm", 0, 5)
display.text("Hi there!", 0, 16)

# x, y, color (0=off, 1=on)
display.pixel(80, 30, 1)

# x, y, length, color
display.hline(0, 40, 100, 1)
display.vline(127, 0, 64, 1)

# x, y, width, height, color
display.fill_rect(20, 50, 50, 20, 1)

display.show()  # Write the contents of the FrameBuffer to display memory

print("Press Ctrl+C to stop.")

try:
    # Forever loop
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    display.poweroff()
