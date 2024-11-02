"""
I2C OLED display SH1106 + DHT12 sensor

MicroPython script for reading data from DHT12 I2C sensor
and displaying on an OLED with the SH1106 controller. The
script requires SH1106 and DHT12 modules, stored in ESP32 device.

Components:
- ESP32-based board
- DHT12 temperature and humidity sensor
- OLED display with SH1106 driver

Authors:
- Robert Hammelrath, https://github.com/robert-hh/SH1106
- Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
- Tomas Fryza

Creation date: 2023-10-27
Last modified: 2024-11-02
"""

from machine import I2C
from machine import Pin
import time
import dht12
from sh1106 import SH1106_I2C

# Init DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = dht12.DHT12(i2c)

# Init OLED display
oled = SH1106_I2C(i2c)
oled.contrast(50)  # Set contrast to 50 %
oled.text("Temp. [C]:", 0, 40)
oled.text("Humid.[%]:", 0, 52)

print(f"I2C configuration : {str(i2c)}")
print("Start using I2C. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        temp, humidity = sensor.read_values()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        oled.fill_rect(85, 38, 120, 50, 0)
        oled.text(f"{temp}", 85, 40)
        oled.text(f"{humidity}", 85, 52)
        oled.show()
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    oled.poweroff()
