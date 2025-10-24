"""
I2C scanner

Scan the I2C (Inter-Integrated Circuit) bus for connected
devices and print results in a 16x8 grid, according to Raspberry Pi
(Linux) `i2cdetect` command.

Authors:
- ChatGPT
- Tomas Fryza

Creation date: 2025-10-24
Last modified: 2025-10-24

 Some known devices:
 - 0x3c - OLED display
 - 0x57 - EEPROM
 - 0x5c - Temp+Humid
 - 0x68 - RTC
 - 0x68 - GY521
 - 0x76 - BME280
 """

from machine import I2C, Pin

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

print("Scanning I2C bus...")
addrs = i2c.scan()

print("    " + " ".join(f"{x:02x}" for x in range(16)))
for high in range(0x00, 0x80, 0x10):
    row = f"{high:02x}:"
    for low in range(16):
        addr = high + low
        if addr < 0x03 or addr > 0x77:
            cell = "  "  # reserved addresses
        elif addr in addrs:
            cell = f"{addr:02x}"
        else:
            cell = "--"
        row += f" {cell}"
    print(row)

if addrs:
    print("\nFound device(s):", ", ".join(f"0x{d:02x}" for d in addrs))
else:
    print("\nNo I2C devices found.")
