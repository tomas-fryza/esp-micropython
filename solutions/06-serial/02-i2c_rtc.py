"""
Read RTC values using I2C bus

This script demonstrates using I2C to read values from
RTC (Real Time Clock) DS3231 device. The script requires
hw_config module, stored in ESP32 device.

Authors:
- MicroPython, https://github.com/micropython/micropython/blob/master/examples/accel_i2c.py
- Tomas Fryza

Creation date: 2024-10-24
Last modified: 2025-10-24
"""

from machine import I2C, Pin
from hw_config import Led
import time

RTC_ADDR = 0x68  # DS3231 I2C address
INIT_TIME = [0x00, 0x22, 0x08]  # (S, M, H)
RTC_UPDATE = False  # Set True to update RTC once

# Addr. #7 |   #6      #5      #4    | #3  #2  #1  #0
#  0:   0  |       10 seconds        |    seconds
#  1:   0  |       10 minutes        |    minutes
#  2:   0  | 12/24 | AM/PM | 10 hour |     hour
#                  | 20 hr |


def bcd_to_int(bcd):
    """Convert BCD byte to integer."""
    return (bcd >> 4) * 10 + (bcd & 0x0F)


def read_rtc_time(i2c, addr):
    """Read time from DS3231 and return tuple (h, m, s)."""
    raw = i2c.readfrom_mem(addr, 0, 3)
    seconds = bcd_to_int(raw[0])
    minutes = bcd_to_int(raw[1])
    hours = bcd_to_int(raw[2] & 0x3F)  # mask 24h mode bits
    return hours, minutes, seconds


# Status LED
led = Led(2)
led.off()

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

if RTC_ADDR not in i2c.scan():
    raise Exception(f"`{hex(RTC_ADDR)}` is not detected")

if RTC_UPDATE:
    print("\nSetting initial time to RTC")
    data = bytearray(INIT_TIME)
    i2c.writeto_mem(RTC_ADDR, 0, data)

print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led.on()
        h, m, s = read_rtc_time(i2c, RTC_ADDR)
        print(f"{h:02}:{m:02}.{s:02}")
        led.off()
        time.sleep(1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
