"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print their addresses (between 0x08 and 0x77
inclusive) in both decimal and hexadecimal formats. This
script is useful for identifying I2C devices connected to
your microcontroller.

Hardware Configuration:
- Connect I2C devices to your ESP32 as follows:
  - SCL (Serial Clock): GPIO 22
  - SDA (Serial Data): GPIO 21
  - VCC: 3.3V
  - GND: GND

Authors: MicroPython
         Tomas Fryza
Date: 2023-06-17
"""

from machine import I2C
from machine import Pin

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

print("Scanning I2C... ", end="")
addrs = i2c.scan()
print(f"{len(addrs)} device(s) detected")

for x in addrs:
    print(f"{x}\t{hex(x)}")
