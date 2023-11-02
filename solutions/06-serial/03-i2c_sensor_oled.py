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
from sh1106 import SH1106_I2C
import time

SENSOR_ADDR = 0x5c
SENSOR_HUMI_REG = 0
SENSOR_TEMP_REG = 2
SENSOR_CHECKSUM = 4


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
    oled.text("2023/24", x=40, y=24)

    oled.text("Tempr. [C]:", x=0, y=40)
    oled.text("Humid. [%]:", x=0, y=52)


# I2C(id, scl, sda, freq)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

# SH1106_I2C(width, height, i2c, addr, rotate)
oled = SH1106_I2C(128, 64, i2c, addr=0x3c, rotate=180)
oled_setup(oled)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")

try:
    while True:
        # readfrom_mem(addr, memaddr, nbytes)
        val = i2c.readfrom_mem(SENSOR_ADDR, SENSOR_HUMI_REG, 4)
        oled.fill_rect(95, 38, 120, 50, 0)
        # Display temperature
        oled.text(f"{val[2]}.{val[3]}", 95, 40)
        # Display humidity
        oled.text(f"{val[0]}.{val[1]}", 95, 52)
        oled.show()
        time.sleep(1)

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
    oled.poweroff()
