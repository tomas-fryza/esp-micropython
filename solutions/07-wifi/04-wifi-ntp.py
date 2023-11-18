import network
import mywifi
import ntptime
from machine import RTC

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
TIMEZONE_OFFSET = 1  # UTC+1:00 ... CET, UTC+2:00 ... CEST

# Create Station interface
wifi = network.WLAN(network.STA_IF)
mywifi.connect(wifi, WIFI_SSID, WIFI_PSWD)

# Get UTC time from NTP server and set it to RTC
ntptime.host = "cz.pool.ntp.org"
ntptime.settime()
print("Local RTC synchronized")
mywifi.disconnect(wifi)

# Create an independent clock object
rtc = RTC()

# Print UTC time after NTP update
print(rtc.datetime())
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
# Update timezone
rtc.init((year, month, day, wday, hrs+TIMEZONE_OFFSET, mins, secs, subsecs))
print(rtc.datetime())

# WRITE YOUR CODE HERE
