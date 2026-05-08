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
Last modified: 2026-05-07
"""

# MicroPython builtin modules
from machine import Pin, I2C
from time import sleep

# External module(s)
from dht12 import DHT12

# Init DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
sensor = DHT12(i2c)

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        temp, humid = sensor.read_values()
        print(f"T={temp} °C, H={humid} %")

        sleep(10)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
