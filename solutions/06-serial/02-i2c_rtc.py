"""
Read RTC values using I2C bus

This script demonstrates using I2C to read values from
RTC (Real Time Clock) device.

Components:
  - ESP32 microcontroller
  - RTC DS3231

Authors: MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
         Tomas Fryza
Creation Date: 2024-10-24
Last Modified: 2024-10-24
"""

from machine import I2C
from machine import Pin
import time
import sys

RTC_ADDR = 0x68  # RTC DS3231
RTC_MIN = 17
RTC_SEC = 20

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
addrs = i2c.scan()
if RTC_ADDR not in addrs:
    raise Exception(f"`{hex(RTC_ADDR)}` is not detected")

print(f"Set initial time to RTC: {RTC_MIN}.{RTC_SEC}")
time_array = bytearray([RTC_SEC, RTC_MIN])
i2c.writeto_mem(RTC_ADDR, 0, time_array)

print("Start using I2C. Press `Ctrl+C` to stop")
print("")

try:
    # Forever loop
    while True:
        # Read 3 bytes from `RTC_ADDR` device, starting at address 0
        a = i2c.readfrom_mem(RTC_ADDR, 0, 2)
        # 0: seconds
        # 1: minutes
        print(f"{a[1]:x}.{a[0]:x}")
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
