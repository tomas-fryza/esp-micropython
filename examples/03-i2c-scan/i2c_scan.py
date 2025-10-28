"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print their addresses. This script is useful
for identifying I2C devices connected to your microcontroller.

Authors:
- MicroPython
- Tomas Fryza

Creation date: 2023-06-17
Last modified: 2024-11-02
"""

from machine import I2C, Pin

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

print("Scanning I2C... ", end="")
addrs = i2c.scan()
print(f"{len(addrs)} device(s) detected")

print("dec.\t hex.")
for addr in addrs:
    print(f"{addr}\t {hex(addr)}")
