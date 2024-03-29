"""
Read sensor values via I2C bus

This MicroPython script demonstrates the initialization
of the I2C bus, the scanning process to locate the DHT12
temperature and humidity sensor assigned to the Slave
address `0x5c`, and the continuous retrieval and printing
of data from the sensor.

Hardware Configuration:
- Connect I2C sensor DHT12 to your ESP32 as follows:
  - SCL: GPIO 22
  - SDA: GPIO 21
  - `+`: 3.3V
  - `-`: GND

Authors: MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
         Tomas Fryza
Date: 2023-06-17
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

print("Stop the code execution by pressing `Ctrl+C` key.")
addrs = i2c.scan()
if SENSOR_ADDR not in addrs:
    raise Exception(f"`{hex(SENSOR_ADDR)}` is not detected")

try:
    while True:
        # readfrom_mem(addr, memaddr, nbytes)
        val = i2c.readfrom_mem(SENSOR_ADDR, SENSOR_TEMP_REG, 2)
        print(f"{val[0]}.{val[1]}°C")
        time.sleep(5)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
