"""
Read BME280 sensor values and send them to ThingSpeak

This script connects to a BME280 sensor and transmits
collected data to ThingSpeak using Wi-Fi via either GET or
POST request.

Requires: wifi_utils, bme280, thingspeak modules and config script

Instructions:
- Go to `https://thingspeak.com` and log in to your account
- Create a new channel with two fields:
  - Field 1: Temperature
  - Field 2: Humidity
- Copy the `Write API Key` -- you will need it here
- Store your Wi-Fi SSID and password to `config.py`

Author(s):
- Tomas Fryza

Creation date: 2023-06-18
Last modified: 2026-06-12
"""

# MicroPython builtin modules
from machine import Pin, I2C
from time import sleep
from network import WLAN, STA_IF

# External modules
from bme280 import BME280
import thingspeak
import wifi_utils
import config

API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
sensor = BME280(i2c)
temp, humid, press, A = sensor.read_values()  # Just take first samples
wifi = WLAN(STA_IF)

try:
    while True:
        temp, humid, press, A = sensor.read_values()
        print(f"T={temp:.1f}°C, H={humid:.1f}%, P={press:.1f}hPa")

        wifi_utils.connect(wifi, config.SSID, config.PSWD)
        thingspeak.send(temp, humid, API_KEY)
        wifi_utils.disconnect(wifi)

        sleep(60)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
    wifi_utils.disconnect(wifi)
