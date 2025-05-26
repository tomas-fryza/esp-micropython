"""
Read DHT12 sensor values and send to ThingSpeak

This script connects to a DHT12 temperature and humidity
sensor and transmits the collected data to ThingSpeak
using Wi-Fi via either GET or POST request.

Requires: wifi_utils, bmp180 modules and config script

Author(s):
- Tomas Fryza

Creation date: 2023-06-18
Last modified: 2025-05-26
"""

from machine import I2C
from machine import Pin


# TODO: Rewrite the code for BMP180 and PIR sensors !!!
import bmp180


import network
import wifi_utils
import config
import urequests
import time

API_KEY = "THINGSPEAK_WRITE_API_KEY"  # Get the key from https://thingspeak.mathworks.com/


def send_to_thingspeak(temp, humidity):
    """
    Send temperature and humidity data to ThingSpeak.

    :param float temp: The temperature value to send.
    :param float humidity: The humidity value to send.
    """
    API_URL = "https://api.thingspeak.com/update"

    # Select GET or POST request
    # Make the GET request
    request_url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={humidity}"
    response = urequests.get(request_url)

    # Make the POST request
    # request_url = f"{API_URL}?api_key={API_KEY}"
    # json = {"field1": temp, "field2": humidity}
    # headers = {"Content-Type": "application/json"}
    # response = urequests.post(request_url, json=json, headers=headers)

    print(f"ThingSpeak entry no.: {response.text}")
    response.close()


# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
# sensor = dht12.DHT12(i2c)

# Create Station interface
wifi = network.WLAN(network.STA_IF)
print("Start using Wi-Fi. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temp, humidity = 20, 30  # sensor.read_values()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")

        wifi_utils.connect(wifi, config.SSID, config.PSWD)
        send_to_thingspeak(temp, humidity)
        wifi_utils.disconnect(wifi)

        time.sleep(60)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    wifi_utils.disconnect(wifi)
