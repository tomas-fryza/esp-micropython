"""
I2C OLED display SH1106 + DHT12 sensor

MicroPython script for initializing I2C and using an OLED
display with the SH1106 controller. The script requires
the SH1106 driver library, stored in ESP32 device.

Hardware Configuration:
- Connect I2C OLED display to your ESP32 as follows:
  - SCL: GPIO 22
  - SDA: GPIO 21
  - VCC: 3.3V
  - GND: GND

Authors: Robert Hammelrath, https://github.com/robert-hh/SH1106
         Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
         Tomas Fryza
Date: 2023-10-27
"""

from machine import I2C
from machine import Pin
import time
import dht12
from sh1106 import SH1106_I2C

WIDTH = 128  # OLED display width
HEIGHT = 64  # OLED display height


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def oled_setup(oled):
    oled.contrast(50)  # Set contrast to 50 %

    # https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
    oled.fill(color=0)  # Clear screen
    oled.fill_rect(x=0, y=0, w=32, h=32, color=1)
    oled.fill_rect(x=2, y=2, w=28, h=28, color=0)
    oled.vline(x=9, y=8, h=22, color=1)
    oled.vline(x=16, y=2, h=22, color=1)
    oled.vline(x=23, y=8, h=22, color=1)
    oled.fill_rect(x=26, y=24, w=2, h=4, color=1)
    oled.text("MicroPython", x=40, y=0)
    oled.text("Brno, CZ", x=40, y=12)
    oled.text("RadioElect.", x=40, y=24)

    oled.text("Tempr. [C]:", x=0, y=40)
    oled.text("Humid. [%]:", x=0, y=52)


# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = dht12.DHT12(i2c)

# Init OLED display
oled = SH1106_I2C(WIDTH, HEIGHT, i2c, rotate=180)
oled_setup(oled)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")

try:
    while True:
        temp, humidity = read_sensor()
        print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        oled.fill_rect(95, 38, 120, 50, 0)
        oled.text(f"{temp}", 95, 40)
        oled.text(f"{humidity}", 95, 52)
        oled.show()
        time.sleep(1)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting...")
    oled.poweroff()
