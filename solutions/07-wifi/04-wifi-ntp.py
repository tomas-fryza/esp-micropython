"""
NTP time synchronization and RTC management
===========================================

This script connects to a Wi-Fi network, synchronizes the
Real-Time Clock (RTC) with an NTP server to obtain the
current UTC time, and then adjusts the RTC to the local
timezone (CET/CEST).

Components:
- ESP32-based board

Author: Tomas Fryza

Creation date: 2023-10-25
Last modified: 2024-11-02
"""

from machine import RTC
import network
import my_wifi
import config
import ntptime
import time

TIMEZONE_OFFSET = 1  # UTC+1:00 for CET (Central European Time)
                     # UTC+2:00 for CEST (Central European Summer Time)

# Create Station interface
wifi = network.WLAN(network.STA_IF)
my_wifi.connect(wifi, config.SSID, config.PSWD)

# Get UTC time from NTP server and set it to RTC
ntptime.host = "cz.pool.ntp.org"
ntptime.settime()
print("Local RTC synchronized")
my_wifi.disconnect(wifi)

# Create an independent clock object
rtc = RTC()

print("UTC time after NTP update:")
print(rtc.datetime())
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print("Update timezone:")
rtc.init((year, month, day, wday, hrs+TIMEZONE_OFFSET, mins, secs, subsecs))
print(rtc.datetime())


# WRITE YOUR CODE HERE


print("Start using RTC. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
        print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")
        time.sleep(1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
