"""
Read DHT12 sensor values and send to ThingSpeak

This script connects to a DHT12 temperature and humidity
sensor and transmits the collected data to ThingSpeak
using Wi-Fi via either GET or POST request.

Author: Tomas Fryza

Creation date: 2023-06-18
Last modified: 2024-11-11
"""

from machine import I2C
from machine import Pin
import dht12
import network
import wifi_module
import config
import urequests
import time

API_KEY = "THINGSPEAK_WRITE_API_KEY"


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

    print(f"Entry # sent to ThingSpeak: {response.text}")
    response.close()


# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = dht12.DHT12(i2c)

# Create Station interface
wifi = network.WLAN(network.STA_IF)
print("Start using Wi-Fi. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temp, humidity = sensor.read_values()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")

        wifi_module.connect(wifi, config.SSID, config.PSWD)
        send_to_thingspeak(temp, humidity)
        wifi_module.disconnect(wifi)

        time.sleep(60)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    wifi_module.disconnect(wifi)
