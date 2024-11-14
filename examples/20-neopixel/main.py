# Complete project details at https://RandomNerdTutorials.com

import machine, neopixel

n = 20
pin = 25

np = neopixel.NeoPixel(machine.Pin(pin), n)

np[0] = (255, 0, 0)
np[3] = (125, 204, 223)
np[7] = (120, 153, 23)
np[10] = (255, 0, 153)
np.write()
