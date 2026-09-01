"""
I2C DHT12 sensor

MicroPython script for reading data from DHT12 I2C sensor
and printing to shell. The script requires DHT12 module, stored
in ESP32 device.

Authors:
- Robert Hammelrath, https://github.com/robert-hh/SH1106
- Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
- Tomas Fryza

Creation date: 2023-10-27
Last modified: 2026-09-01
"""

# MicroPython builtin modules
from machine import Pin, I2C
from time import sleep

# External module(s)
from dht12 import DHT12
from bme280 import BME280

# Init sensor
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
sensor = DHT12(i2c)  # 1st variant
# sensor = BME280(i2c)  # 2nd variant

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        temp, humid = sensor.read_values()  # 1st variant
        # temp, humid, P, A = sensor.read_values()  # 2nd variant
        print(f"T={temp:.1f}°C, H={humid:.1f}%")
        # print(P, A)

        sleep(10)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
