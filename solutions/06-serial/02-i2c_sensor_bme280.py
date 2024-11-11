"""
Read values from BME280 sensor (Pressure, Temperature, Humidity)

This script demonstrates using I2C to read values from
BME280 pressure, temperature, and humidity sensor. The
script requires BME280 module, stored in ESP32 device.

Authors:
- https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/
- Tomas Fryza

Creation date: 2023-11-01
Last modified: 2024-11-02
"""

from machine import I2C
from machine import Pin
import time
import bme280

# Init BME280 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
bme = bme280.BME280(i2c=i2c)

print(f"I2C configuration : {str(i2c)}")
print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temp = bme.temperature  # Return temp in degrees C
        hum = bme.humidity
        pres = bme.pressure
        print(f"Temperature: {temp}")
        print(f"Humidity: {hum}")
        print(f"Pressure: {pres}")
        time.sleep(5)
        print("")

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
