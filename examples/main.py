
# https://wiki.dfrobot.com/FireBeetle_Board_ESP32_E_SKU_DFR0654
# https://docs.micropython.org/en/latest/library/neopixel.html

import machine
import neopixel
import time


p = machine.Pin(5)
n = neopixel.NeoPixel(p, 1)

# Draw a red gradient
for i in range(32):
    n = (i * 8, 0, 0)
    time.sleep(.1)

    # Update the strip.
    n.write()
