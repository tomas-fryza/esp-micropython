"""
ESP32 RTC Clock Sync with NTP and Timezone Offset

This script connects to Wi-Fi, synchronizes the ESP32's RTC with
an NTP server, adjusts for a specified timezone offset (CET/CEST),
and prints the local time periodically.

Requires: wifi_utils module and config script

Author(s):
- Tomas Fryza

Creation date: 2023-10-25
Last modified: 2025-05-28
"""

from machine import RTC
import network
import wifi_utils
import config
import ntptime
import time

TIMEZONE_OFFSET = 2  # CEST, Central European Summer Time (UTC+2)
                     # CET, Central European Time (UTC+1)


def sync_time():
    print("Connecting to Wi-Fi...")
    wifi = network.WLAN(network.STA_IF)
    wifi_utils.connect(wifi, config.SSID, config.PSWD)

    try:
        ntptime.host = "cz.pool.ntp.org"
        ntptime.settime()
        print("NTP time synchronized.")
    except Exception as e:
        print("Failed to sync time via NTP:", e)
    finally:
        wifi_utils.disconnect(wifi)
        print("Wi-Fi disconnected.")


def apply_timezone_offset(rtc):
    (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
    hrs = (hrs + TIMEZONE_OFFSET) % 24  # wrap around 24-hour clock
    rtc.init((year, month, day, wday, hrs, mins, secs, subsecs))
    print("Timezone offset applied.")


def print_current_time(rtc):
    (year, month, day, wday, hrs, mins, secs, _) = rtc.datetime()
    print(f"{year:04d}-{month:02d}-{day:02d} {hrs:02d}:{mins:02d}:{secs:02d}")


rtc = RTC()
sync_time()
print("RTC after NTP sync (UTC):")
print(rtc.datetime())

apply_timezone_offset(rtc)
print("RTC with timezone offset:")
print(rtc.datetime())

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        print_current_time(rtc)
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
