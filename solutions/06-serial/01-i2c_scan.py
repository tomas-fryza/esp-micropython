"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print their addresses. This script is useful
for identifying I2C devices connected to your microcontroller.

Components:
  - ESP32 microcontroller
  - several I2C devices

Authors: MicroPython, Tomas Fryza
Creation Date: 2023-06-17
Last Modified: 2024-10-18
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
