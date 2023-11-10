"""
I2C BME280 sensor (Pressure, Temperature, Humidity)

TBD

Hardware Configuration:
- Connect I2C BME280 sensor to your ESP32 as follows:
  - SCL: GPIO 22
  - SDA: GPIO 21
  - VIN: 3.3V
  - GND: GND

Authors: https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
         Tomas Fryza
Date: 2023-11-01
"""

from machine import Pin
from machine import I2C
from time import sleep
import bme280

# I2C(id, scl, sda, freq)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
bme = bme280.BME280(i2c=i2c, addr=0x76)

try:
    while True:
        temp = bme.temperature  # Return temp in degrees
        hum = bme.humidity()
        pres = bme.pressure()

        print(f'Temperature: {temp}')
        print(f'Humidity: {hum}')
        print(f'Pressure: {pres}')

        sleep(5)
        print("")

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
