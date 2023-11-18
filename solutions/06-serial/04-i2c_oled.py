"""
I2C OLED display SH1106

MicroPython script for initializing I2C and using an OLED
display with the SH1106 controller. The script requires
the SH1106 driver library, stored in ESP32 device.

Hardware Configuration:
- Connect I2C OLED display to your ESP32 as follows:
  - SCL: GPIO 22
  - SDA: GPIO 21
  - VCC: 3.3V
  - GND: GND

Authors:
  Robert Hammelrath, https://github.com/robert-hh/SH1106
  Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
  Raspberry Pi, https://github.com/raspberrypi/pico-micropython-examples/blob/master/i2c/1106oled/i2c_1106oled_with_freq.py
  Tomas Fryza
Date: 2023-10-27
"""

from machine import I2C
from machine import Pin
from sh1106 import SH1106_I2C

WIDTH = 128  # OLED display width
HEIGHT = 64  # OLED display height

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
print(f"I2C address       : {hex(i2c.scan()[0])}")
print(f"I2C configuration : {str(i2c)}")

# Init OLED display
oled = SH1106_I2C(WIDTH, HEIGHT, i2c, rotate=180)

# Add some text
oled.text("Using OLED and", x=0, y=40)
oled.text("ESP32", x=50, y=50)


# WRITE YOUR CODE HERE


# Finally update the OLED display so the text is displayed
oled.show()
