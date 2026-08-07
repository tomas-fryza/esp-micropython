"""
Joystick readout demo

MicroPython script for reading values from a two-axis joystick
connected to ADC pins on a Raspberry Pi Pico W and printing
the measured positions to the shell. The script uses the ADC
and Pin modules from the machine library.

Authors:
- https://peppe8o.com/analog-joystick-with-raspberry-pi-pico-and-micropython/
- Tomas Fryza

Creation date: 2026-08-07
Last modified: 2026-08-07
"""

from machine import ADC, Pin
from time import sleep

xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))

readDelay = 0.5

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        xRef = xAxis.read_u16()
        yRef = yAxis.read_u16()

        print(f"x: {xRef} \ty: {yRef}")

        sleep(readDelay)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
