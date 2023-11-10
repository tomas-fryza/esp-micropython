from machine import I2C
from machine import Pin
import time
import dht12
import network
import wifi_con
import urequests  # Network Request Module

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
THINGSPEAK_API_KEY = "<THINGSPEAK WRITE API KEY>"

# Create Station interface
wifi = network.WLAN(network.STA_IF)

# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
sensor = dht12.DHT12(i2c)


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


try:
    while True:
        temp, humidity = 0, 1  # read_sensor()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        wifi_con.connect(wifi, WIFI_SSID, WIFI_PSWD)
        # send_to_thingspeak(temp, humidity)
        wifi_con.disconnect(wifi)
        time.sleep(60)

        # TODO:
        # def send_to_thingspeak(temp, humidity):
        #     url = f"{api_url}?api_key={api_key}&field1={temp}&field2={humidity}"
        #     response = urequests.get(url)
        #     print("Response:", response.text)
        #     response.close()


        # connect_wifi()
        #
        # Send data using a POST request
        # request = urequests.post(
        #     'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_API_KEY,
        #     json={"field1": temp, "field2": humi},
        #     headers={"Content-Type": "application/json"})
        # print(f"Response: {request.text}")
        # request.close()
        #
        # disconnect_wifi()

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
