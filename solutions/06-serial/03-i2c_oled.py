"""
I2C OLED display SH1106

MicroPython script for initializing I2C and using an OLED
display with the SH1106 controller. The script requires
the SH1106 driver library, stored in ESP32 device.

Hardware Configuration:
- Connect I2C OLED display to your ESP32 as follows:
  - SCL: GPIO pin 22
  - SDA: 21
  - VCC: 3.3V
  - GND: GND

Authors: Robert Hammelrath, https://github.com/robert-hh/SH1106
         Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
         Tomas Fryza
Date: 2023-10-27
"""

from machine import I2C
from machine import Pin
from sh1106 import SH1106_I2C
import time

# I2C(id, scl, sda, freq)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

# SH1106_I2C(width, height, i2c, addr, rotate)
display = SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)
display.contrast(100)  # Set contrast to 50 %

display.text("Using OLED...", x=0, y=0)
display.show()

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")

try:
    while True:
        time.sleep(.1)

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
    display.poweroff()
