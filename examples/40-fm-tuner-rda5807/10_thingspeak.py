"""
Read BMP180 sensor values and send them to ThingSpeak

This script connects to a BMPT180 temperature and pressure
sensor and transmits the collected data to ThingSpeak
using Wi-Fi via either GET or POST request.

Requires: wifi_utils, bmp180 modules and config script

Instructions:
- Go to `https://thingspeak.com` and log in to your account
- Create a new channel with two fields:
  - Field 1: Temperature
  - Field 2: Pressure
- Copy the `Write API Key` -- you will need it here
- Store your Wi-Fi SSID and password to `config.py`

Author(s):
- Tomas Fryza

Creation date: 2023-06-18
Last modified: 2025-06-01
"""

# MicroPython builtin modules
from machine import Pin
from machine import SoftI2C
import time
import network
import urequests

# External modules
from bmp180 import BMP180
import wifi_utils
import config

API_KEY = "THINGSPEAK_WRITE_API_KEY"


def send_to_thingspeak(temp, press):
    """
    Send temperature and pressure data to ThingSpeak.

    :param float temp: The temperature value to send.
    :param float press: The pressure value to send.
    """
    API_URL = "https://api.thingspeak.com/update"

    # Select GET or POST request
    # Make the GET request
    request_url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={press}"
    try:
        response = urequests.get(request_url)
        print("Status code:", response.status_code)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Error sending data:", e)
        response = urequests.get(request_url)

    # Make the POST request
    # request_url = f"{API_URL}?api_key={API_KEY}"
    # json = {"field1": temp, "field2": press}
    # headers = {"Content-Type": "application/json"}
    # response = urequests.post(request_url, json=json, headers=headers)
    # print(f"ThingSpeak entry no.: {response.text}")
    # response.close()


# Connect to the BMP180 sensor
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
bmp180 = BMP180(i2c)

# Create Station interface
wifi = network.WLAN(network.STA_IF)
print("Start using Wi-Fi. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temperature = bmp180.temperature
        pressure = bmp180.pressure/100
        altitude = bmp180.altitude

        print(f"{temperature:.1f} C\t {pressure:.1f} hPa\t {altitude:.1f} m")

        wifi_utils.connect(wifi, config.SSID, config.PSWD)
        send_to_thingspeak(temperature, pressure)
        wifi_utils.disconnect(wifi)

        time.sleep(60)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    wifi_utils.disconnect(wifi)
