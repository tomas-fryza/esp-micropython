"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print their addresses. This script is useful
for identifying I2C devices connected to your microcontroller.

Authors:
- MicroPython
- Tomas Fryza

Creation date: 2023-06-17
Last modified: 2026-07-23

Some known devices:
- 0x3c - OLED display
- 0x57 - EEPROM
- 0x5c - DHT Temperature & Humidity
- 0x5d - TFT touch screen
- 0x68 - RTC
- 0x68 - GY521
- 0x70 - SHTC3 Temperature & Humidity
- 0x76 - BME280 Pressure, Temperature, Humidity
"""

from machine import I2C, Pin

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)

print("Scanning I2C... ", end="")
addrs = i2c.scan()
print(f"{len(addrs)} device(s) detected")

if len(addrs) > 0:
    print("dec.\t hex.")
    for addr in addrs:
        print(f"{addr}\t {hex(addr)}")
