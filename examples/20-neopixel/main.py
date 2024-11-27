# https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html

from machine import Pin
from neopixel import NeoPixel
import time

def demo(np):
    n_leds = np.n
    print(f"{n_leds} LEDs")

    print("cycle")
    for i in range(1 * n_leds):
        for j in range(n_leds):
            np[j] = (0, 0, 0)
        np[i % n_leds] = (255, 255, 255)
        np.write()
        time.sleep_ms(125)

    print("bounce")
    for i in range(1 * n_leds):
        for j in range(n_leds):
            np[j] = (0, 0, 128)
        if (i // n_leds) % 2 == 0:
            np[i % n_leds] = (0, 0, 0)
        else:
            np[n_leds - 1 - (i % n_leds)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    print("fade in/out")
    for i in range(0, 4 * 256, 8):
        for j in range(n_leds):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    print("clear")
    for i in range(n_leds):
        np[i] = (0, 0, 0)
    np.write()

# Vcc
# GND
# 15/A4 (FireBeetle v2)
np = NeoPixel(Pin(15), 60)  # 60 LEDs
demo(np)
