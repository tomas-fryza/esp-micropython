"""
I2C BME280 sensor (Pressure, Temperature, Humidity)

TBD

Components:
  - ESP32 microcontroller
  - BME280 pressure, temperature, and humidity sensor

Authors: https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
         Tomas Fryza
Date: 2023-11-01
"""

from machine import Pin
from machine import I2C
from time import sleep
import bme280

# Init I2C using pins GP22 & GP21 (default I2C0 pins)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
print(f"I2C address       : {hex(i2c.scan()[0])}")
print(f"I2C configuration : {str(i2c)}")

# Init BME280 sensor
bme = bme280.BME280(i2c=i2c)

try:
    while True:
        temp = bme.temperature  # Return temp in degrees
        hum = bme.humidity
        pres = bme.pressure

        print(f"Temperature: {temp}")
        print(f"Humidity: {hum}")
        print(f"Pressure: {pres}")

        sleep(5)
        print("")

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
