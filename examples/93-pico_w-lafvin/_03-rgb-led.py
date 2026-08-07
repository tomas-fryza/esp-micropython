"""
RGB LED diagnostic test

Simple MicroPython test for a single RGB NeoPixel LED. The
script uses a short color sequence with visible delays.

Note:
If the LED still flickers or does not light reliably, add a
100 nF capacitor between V+ and GND close to the LED and a
330 ohm resistor in series with the data line.
"""

from machine import Pin
import neopixel
import time

np = neopixel.NeoPixel(Pin(12), 1, timing=1)


def show(color, delay_ms=500):
    np[0] = color
    np.write()
    np.write()
    time.sleep_ms(delay_ms)


# Start with a short reset
show((0, 0, 0), 100)

# Test the LED with a simple color sequence
show((255, 0, 0), 800)  # Red
show((0, 255, 0), 800)  # Green
show((0, 0, 255), 800)  # Blue
show((255, 255, 255), 800)  # White
show((0, 0, 0), 500)  # Turn off
