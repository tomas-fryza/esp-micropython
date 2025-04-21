
# https://wiki.dfrobot.com/FireBeetle_Board_ESP32_E_SKU_DFR0654
# https://docs.micropython.org/en/latest/library/neopixel.html

from machine import Pin
from neopixel import NeoPixel
import time


np = NeoPixel(Pin(2), 1)

# Draw a red gradient
for i in range(16):
    np[0] = (i*8, 0, 0)
    np.write()
    time.sleep(.1)

np[0] = (128, 128, 0)
np.write()
time.sleep(1)

np[0] = (0, 128, 0)
np.write()
time.sleep(1)

np[0] = (0, 128, 128)
np.write()
time.sleep(1)

np[0] = (0, 0, 128)
np.write()
time.sleep(1)

np[0] = (128, 0, 128)
np.write()
time.sleep(1)

np[0] = (128, 0, 0)
np.write()
time.sleep(1)

np[0] = (0, 0, 0)
np.write()
