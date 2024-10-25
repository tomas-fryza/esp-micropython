"""
Read RTC values using I2C bus

This script demonstrates using I2C to read values from
RTC (Real Time Clock) DS3231 device.

Components:
  - ESP32 microcontroller
  - RTC DS3231

Authors: MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
         Tomas Fryza
Creation Date: 2024-10-24
Last Modified: 2024-10-25
"""

from machine import I2C
from machine import Pin
from io_control import Led
import time

RTC_ADDR = 0x68  # RTC DS3231
RTC_HRS = 0x08
RTC_MIN = 0x22
RTC_SEC = 0x00
RTC_UPDATE = False
# Addr. #7 |   #6      #5      #4    | #3  #2  #1  #0
#  0:   0  |       10 seconds        |    seconds
#  1:   0  |       10 minutes        |    minutes
#  2:   0  | 12/24 | AM/PM | 10 hour |     hour
#                  | 20 hr |

led = Led(2)
led.off()

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
addrs = i2c.scan()
if RTC_ADDR not in addrs:
    raise Exception(f"`{hex(RTC_ADDR)}` is not detected")

if RTC_UPDATE:
    print("")
    print(f"Set initial time: {RTC_HRS:x}.{RTC_MIN:x}.{RTC_SEC:x}")
    time_array = bytearray([RTC_SEC, RTC_MIN, RTC_HRS])
    i2c.writeto_mem(RTC_ADDR, 0, time_array)

print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led.toggle()
        # Read 3 bytes from `RTC_ADDR` device, starting at address 0
        a = i2c.readfrom_mem(RTC_ADDR, 0, 3)
        print(f"{a[2]:x}:{a[1]:x}.{a[0]:x}")
        led.toggle()
        time.sleep(1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
