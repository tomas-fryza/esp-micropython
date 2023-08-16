"""Set internal RTC using the NTP server.

Use Network Time Protocol (NTP) via Wi-Fi for synchronizing time
of Real Time Clock (RTC) and providing an accurate local time.

NOTES:
    * Set your Wi-Fi SSID and password
    * Set your time zone

TODOs:
    * Add comments to all functions

Inspired by:
    * https://www.engineersgarage.com/micropython-esp8266-esp32-rtc-utc-local-time/
    * https://github.com/micropython/micropython-lib/blob/master/micropython/net/ntptime/ntptime.py
    * https://docs.micropython.org/en/latest/library/machine.RTC.html#machine-rtc
    * https://www.epochconverter.com/
"""

from machine import RTC
import network
import ntptime
from time import localtime, sleep


def connect_wifi():
    from time import sleep_ms

    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")

        # Activate station/Wi-Fi client interface
        sta_if.active(True)

        # Connect
        sta_if.connect(WIFI_SSID, WIFI_PSWD)

        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")


def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
UTC_OFFSET = 2  # CEST is UTC+2:00

# Create an independent clock object
rtc = RTC()

# Create Station interface
sta_if = network.WLAN(network.STA_IF)
connect_wifi()

# Get UTC time from NTP server (pool.ntp.org) and store it
# to internal RTC
ntptime.settime()

# Display UTC (Coordinated Universal Time / Temps Universel Coordonné)
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print(f"UTC Time: {year}-{month}-{day} {hrs}:{mins}:{secs}")

# Get epoch time in seconds (for timezone update)
sec = ntptime.time()

disconnect_wifi()

# Update your epoch time in seconds and store in to internal RTC
sec = int(sec + UTC_OFFSET * 60 * 60)
(year, month, day, hrs, mins, secs, wday, yday) = localtime(sec)
rtc.datetime((year, month, day, wday, hrs, mins, secs, 0))

print(f"Local RTC time: UTC+{UTC_OFFSET}:00")

# Forever loop
while True:
    # Read values from internal RTC
    (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
    print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")

    # Delay 30 seconds
    sleep(30)
