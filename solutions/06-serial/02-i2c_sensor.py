"""
Read sensor values using I2C bus

This script demonstrates using I2C to read values from
DHT12 temperature and humidity sensor.

Authors:
- MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
- Tomas Fryza

Creation date: 2023-06-17
Last modified: 2024-11-02
"""

from machine import I2C
from machine import Pin
import time

SENSOR_ADDR = 0x5c  # DHT12

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

# Check the sensor
addrs = i2c.scan()
if SENSOR_ADDR not in addrs:
    raise Exception(f"`{hex(SENSOR_ADDR)}` is not detected")

print(f"I2C configuration : {str(i2c)}")
print("Start using I2C. Press `Ctrl+C` to stop")
print("")
print("humidity\t temperature\t checksum")

try:
    # Forever loop
    while True:
        # Read 2 bytes from `SENSOR_ADDR` device, starting at address 0
        a = i2c.readfrom_mem(SENSOR_ADDR, 0, 5)
        print(f"{a[0]}.{a[1]} %\t\t {a[2]}.{a[3]} C\t\t {a[4]}")

        if (a[0]+a[1]+a[2]+a[3]) & 0xff != a[4]:
            raise Exception("Checksum error")
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
