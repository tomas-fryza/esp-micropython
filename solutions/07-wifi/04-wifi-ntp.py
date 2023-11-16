import network
import mywifi
import ntptime
from machine import RTC
import time

# Network settings
# WIFI_SSID = "<YOUR WIFI SSID>"
# WIFI_PSWD = "<YOUR WIFI PASSWORD>"
UTC_OFFSET = 1  # CEST is UTC+2:00
                # CET is UTC+1:00

# Create an independent clock object
rtc = RTC()

# Print time after power on
print(f"RTC time: {rtc.datetime()}")

# Create Station interface
wifi = network.WLAN(network.STA_IF)
mywifi.connect(wifi, WIFI_SSID, WIFI_PSWD)

# Get UTC time from NTP server (pool.ntp.org) and set it
# to the internal RTC
ntptime.settime()
print("Local RTC synchronized")
mywifi.disconnect(wifi)

# Print time after NTP update
print(f"RTC time: {rtc.datetime()}")
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
# Print it in more friendly way
print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")



# TODO: Apply time zone



# Display UTC (Coordinated Universal Time / Temps Universel Coordonné)
# (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
# print(f"UTC Time: {year}-{month}-{day} {hrs}:{mins}:{secs}")

# Get epoch time in seconds (for timezone update)
# sec = ntptime.time()


# Update your epoch time in seconds and store in to internal RTC
# sec = int(sec + UTC_OFFSET * 60 * 60)
# (year, month, day, hrs, mins, secs, wday, yday) = time.localtime(sec)
# rtc.datetime((year, month, day, wday, hrs, mins, secs, 0))

# print(f"Local RTC time: UTC+{UTC_OFFSET}:00")

try:
    while True:
        print(f"RTC time: {rtc.datetime()}")
        (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
        print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")
        time.sleep(2)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
    mywifi.disconnect(wifi)
