from machine import Pin
import neopixel
import time

np = neopixel.NeoPixel(Pin(12), 1)

# Turn off
np[0] = (0, 0, 0)
np.write()
time.sleep_ms(100)

# Red
np[0] = (255, 0, 0)
np.write()
