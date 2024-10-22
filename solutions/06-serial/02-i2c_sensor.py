"""
Read sensor values using I2C bus

This script demonstrates using I2C to read values from
DHT12 temperature and humidity sensor.

Authors: MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
         Tomas Fryza
Creation Date: 2023-06-17
Last Modified: 2024-10-18
"""

from machine import I2C
from machine import Pin
import time

SENSOR_ADDR = 0x5c
SENSOR_HUMI_REG = 0
SENSOR_TEMP_REG = 2
SENSOR_CHECKSUM = 4

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
# Display device address
print(f"I2C address       : {hex(i2c.scan()[0])}")
# Display I2C config
print(f"I2C configuration : {str(i2c)}")

addrs = i2c.scan()
if SENSOR_ADDR not in addrs:
    raise Exception(f"`{hex(SENSOR_ADDR)}` is not detected")

print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
                # readfrom_mem(addr, memaddr, nbytes)
        val = i2c.readfrom_mem(SENSOR_ADDR, SENSOR_TEMP_REG, 2)
        print(f"{val[0]}.{val[1]}°C")
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
