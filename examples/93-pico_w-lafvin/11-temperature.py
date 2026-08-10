"""
I2C BME280 sensor

MicroPython script for reading data from BME280 I2C sensor
and printing to shell. The script requires BME280 module, stored
in MicroPython device.

Authors:
- Robert Hammelrath, https://github.com/robert-hh/SH1106
- Martin Fitzpatrick, https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/
- Tomas Fryza
- Codex (OpenAI)

Creation date: 2023-10-27
Last modified: 2026-08-07
"""

# MicroPython builtin modules
from machine import Pin, I2C
from time import sleep

# External module(s)
from bme280 import BME280

BME280_ADDR = 0x76
READ_INTERVAL_S = 10

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100_000)
addrs = i2c.scan()

# Check: Stop if specifically the BME280 is missing
if BME280_ADDR not in addrs:
    detected = [hex(address) for address in addrs]
    print(f"Error: BME280 not found. Detected devices: {detected}")
    raise SystemExit

sensor = BME280(i2c)
temp, humid, press, A = sensor.read_values()  # Just read first samples
sleep(1)

print()
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        temperature, humidity, pressure, altitude = sensor.read_values()

        print(
            f"Temperature: {temperature:.1f} °C, "
            f"Humidity: {humidity:.1f} %, "
            f"Pressure: {pressure:.1f} hPa"
        )
        sleep(READ_INTERVAL_S)

        sleep(10)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
