"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print their addresses. This script is useful
for identifying I2C devices connected to your microcontroller.

Authors:
- MicroPython
- Tomas Fryza

Creation date: 2023-06-17
Last modified: 2025-02-25

Scanning I2C... 7 device(s) detected
dec. hex.
16   0x10 -- rda5807 (sequential access / RDA5800 mode)
17   0x11 -- rda5807 (random access / RDA5807 mode !!!)
35   0x23 -- bh1750 (light sensor)
60   0x3c -- OLED (!!!)
96   0x60 -- rda5807 (TEA5767 compatible mode)
104  0x68 -- mpu6050 (accel/gyro/temp)
119  0x77 -- bmp180 (pressure/temperature !!!)
"""

from machine import I2C
from machine import Pin

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

print("Scanning I2C... ", end="")
addrs = i2c.scan()
print(f"{len(addrs)} device(s) detected")

print("dec.\t hex.")
for addr in addrs:
    print(f"{addr}\t {hex(addr)}")
