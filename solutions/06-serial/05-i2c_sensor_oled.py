"""
I2C OLED display SH1106 + DHT12 sensor

MicroPython script for reading data from DHT12 I2C sensor
and displaying on an OLED with the SH1106 controller. The
script requires SH1106 and DHT12 modules, stored in ESP32 device.

Components:
  - ESP32 microcontroller
  - DHT12 temperature and humidity sensor
  - OLED display with SH1106 driver

Authors: Robert Hammelrath, https://github.com/robert-hh/SH1106
         Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
         Tomas Fryza
Creation Date: 2023-10-27
Last Modified: 2024-10-22
"""

from machine import I2C
from machine import Pin
import time
import dht12
from sh1106 import SH1106_I2C
import sys


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def oled_setup(oled):
    oled.contrast(50)  # Set contrast to 50 %
    oled.text("Tempr. [C]:", 0, 40)
    oled.text("Humid. [%]:", 0, 52)


# Init DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = dht12.DHT12(i2c)

# Init OLED display
oled = SH1106_I2C(i2c)
oled_setup(oled)

print(f"I2C configuration : {str(i2c)}")
print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temp, humidity = read_sensor()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        oled.fill_rect(95, 38, 120, 50, 0)
        oled.text(f"{temp}", 95, 40)
        oled.text(f"{humidity}", 95, 52)
        oled.show()
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    oled.poweroff()

    # Stop program execution
    sys.exit(0)
