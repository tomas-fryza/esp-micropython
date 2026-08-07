"""
I2C DHT12 sensor

MicroPython script for reading data from BME280 I2C sensor
and printing to shell. The script requires BME280 module, stored
in MicroPython device.

Authors:
- Robert Hammelrath, https://github.com/robert-hh/SH1106
- Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
- Tomas Fryza

Creation date: 2023-10-27
Last modified: 2026-08-06
"""

# MicroPython builtin modules
from machine import Pin, I2C
from time import sleep
import sys

# External module(s)
from bme280 import BME280

# Common BME280 address: 0x76 (118 dec)
BME280_ADDR = 0x76

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)
addrs = i2c.scan()

# Check: Stop if specifically the BME280 is missing
if BME280_ADDR not in addrs:
    print(f"Error: BME280 not found. Detected devices: {[hex(a) for a in addrs]}")
    sys.exit()

sensor = BME280(i2c)
temp, humid, press, A = sensor.read_values()  # Just take first samples
sleep(1)

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        temp, humid, press, A = sensor.read_values()
        print(f"T={temp:.1f}°C, H={humid:.1f}%, P={press:.1f}hPa")

        sleep(10)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
