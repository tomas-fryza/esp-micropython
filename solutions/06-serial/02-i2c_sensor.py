"""
Read sensor values using I2C bus

This script demonstrates using I2C to read values from
DHT12 temperature and humidity sensor.

Components:
  - ESP32 microcontroller
  - DHT12 temperature and humidity sensor

Authors: MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
         Tomas Fryza
Creation Date: 2023-06-17
Last Modified: 2024-10-22
"""

from machine import I2C
from machine import Pin
import time
import sys

SENSOR_ADDR = 0x5c

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

# Check the sensor
addrs = i2c.scan()
if SENSOR_ADDR not in addrs:
    raise Exception(f"`{hex(SENSOR_ADDR)}` is not detected")

print(f"I2C configuration : {str(i2c)}")
print("Start using I2C. Press `Ctrl+C` to stop")
print("humidity\t temperature\t checksum")

try:
    # Forever loop
    while True:
        # Read 2 bytes from `SENSOR_ADDR` device, starting at address 0
        val = i2c.readfrom_mem(SENSOR_ADDR, 0, 5)
        print(f"{val[0]}.{val[1]} %\t\t {val[2]}.{val[3]} C\t\t {val[4]}")

        if (val[0]+val[1]+val[2]+val[3]) & 0xff != val[4]:
            raise Exception("Checksum error")
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
