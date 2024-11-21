from machine import Pin
from neopixel import NeoPixel
import time

n_leds = 60
data_pin = 25

np = NeoPixel(Pin(data_pin), n_leds)

for i in range(n_leds):
    np[i] = (255, 0, 0)
    np.write()
    print(f"LED #{i}")
    time.sleep_ms(250)
