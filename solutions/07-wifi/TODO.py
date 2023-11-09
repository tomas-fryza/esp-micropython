import dht12
import urequests
import time
from machine import I2C, Pin

# Connect to the DHT12 sensor
i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = dht12.DHT12(i2c)

# ThingSpeak API Key and URL
api_key = "YOUR_THINGSPEAK_API_KEY"
api_url = "https://api.thingspeak.com/update"

def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()

def send_to_thingspeak(temp, humidity):
    url = f"{api_url}?api_key={api_key}&field1={temp}&field2={humidity}"
    response = urequests.get(url)
    print("Response:", response.text)
    response.close()

while True:
    temp, humidity = read_sensor()
    print(f"Temperature: {temp}°C, Humidity: {humidity}%")
    send_to_thingspeak(temp, humidity)
    time.sleep(300)  # Wait for 5 minutes
