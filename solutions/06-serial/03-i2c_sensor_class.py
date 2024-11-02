from machine import I2C
from machine import Pin
import time
import dht12


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = dht12.DHT12(i2c)

try:
    while True:
        temp, humidity = read_sensor()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        time.sleep(5)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
