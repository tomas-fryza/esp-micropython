"""
Read the X and Y positions of an analog joystick.

Wiring:
- VRx -> GPIO 26 / ADC0
- VRy -> GPIO 27 / ADC1
- VCC -> 3.3 V
- GND -> GND

The ADC readings range from 0 to 65535.

Authors:
- https://peppe8o.com/analog-joystick-with-raspberry-pi-pico-and-micropython/
- Tomas Fryza
- Codex (OpenAI)

Creation date: 2026-08-07
Last modified: 2026-08-07
"""

from machine import ADC, Pin
from time import sleep

X_AXIS_PIN = 26
Y_AXIS_PIN = 27
READ_INTERVAL_S = 0.5

x_axis = ADC(Pin(X_AXIS_PIN))
y_axis = ADC(Pin(Y_AXIS_PIN))

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        x_value = x_axis.read_u16()
        y_value = y_axis.read_u16()

        print(f"X: {x_value:5d}  Y: {y_value:5d}")
        sleep(READ_INTERVAL_S)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
