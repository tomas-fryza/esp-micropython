from machine import I2C
from machine import Pin
import time
import dht12
import network
import mywifi
import urequests  # Network Request Module

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
API_KEY = "<THINGSPEAK WRITE API KEY>"

# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
sensor = dht12.DHT12(i2c)

# Create Station interface
wifi = network.WLAN(network.STA_IF)


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def send_to_thingspeak(temp, humidity):
    API_URL = "https://api.thingspeak.com/update"

    # Select GET or POST request
    # GET request
    request_url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={humidity}"
    response = urequests.get(request_url)

    # POST request
    # request_url = f"{API_URL}?api_key={API_KEY}"
    # json = {"field1": temp, "field2": humidity}
    # headers = {"Content-Type": "application/json"}
    # response = urequests.post(request_url, json=json, headers=headers)

    print(f"Response from ThingSpeak: {response.text}")
    response.close()


try:
    while True:
        temp, humidity = read_sensor()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        mywifi.connect(wifi, WIFI_SSID, WIFI_PSWD)
        send_to_thingspeak(temp, humidity)
        mywifi.disconnect(wifi)
        time.sleep(60)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
    mywifi.disconnect(wifi)
