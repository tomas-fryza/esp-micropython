"""
I2C OLED display SH1106 + DHT12 sensor

MicroPython script for reading data from DHT12 I2C sensor
and displaying on an OLED with the SH1106 controller. The
script requires SH1106 and DHT12 modules, stored in ESP32 device.

Authors:
- Robert Hammelrath, https://github.com/robert-hh/SH1106
- Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
- Tomas Fryza

Creation date: 2023-10-27
Last modified: 2026-05-07
"""

# MicroPython builtin modules
from machine import I2C, Pin, I2C
from time import sleep

# External modules
from dht12 import DHT12
from bme280 import BME280
from sh1106 import SH1106_I2C

# Init DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
sensor = DHT12(i2c)  # 1st variant
# sensor = BME280(i2c)  # 2nd variant

# Init OLED display
display = SH1106_I2C(i2c)
display.text("Temp. [C]:", 0, 40)
display.text("Humid.[%]:", 0, 52)

led = Pin(2, Pin.OUT)

print("Read temperature and humidity every 10 secs.")
print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        led.on()
        temp, humid = sensor.read_values()  # 1st variant
        # temp, humid, P, A = sensor.read_values()  # 2nd variant
        print(f"T={temp:.1f}°C, H={humid:.1f}%")

        display.fill_rect(85, 38, 120, 50, 0)
        display.text(f"{temp:.1f}", 85, 40)
        display.text(f"{humid:.1f}", 85, 52)
        display.show()
        led.off()

        sleep(10)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")

    # Optional cleanup code
    display.poweroff()
    led.off()
