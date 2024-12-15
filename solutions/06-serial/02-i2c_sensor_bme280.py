"""
This script uses I2C to read temperature, humidity, and
pressure from the BME280 sensor.

Authors
-------
- `RandomNerdTutorials.com <https://randomnerdtutorials.com/micropython-bme280-esp32-esp8266/>`_
- Tomas Fryza

Modification history
--------------------
- **2024-12-13** : bme280 method `read_values()` added.
- **2023-11-01** : Example created.
"""

from machine import I2C
from machine import Pin
import time
import bme280

# Connect to the BME280 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
bme = bme280.BME280(i2c)

# Ignore the first measurement
T, RH, P, A = bme.read_values()
time.sleep(1)

print(f"I2C configuration: {str(i2c)}")
print("")
print("Start measuring. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        T, RH, P, A = bme.read_values()
        print(f"Temperature     [°C] : {T:.1f}")
        print(f"Humidity         [%] : {RH:.1f}")
        print(f"Pressure       [hPa] : {P:.1f}")
        print(f"Approx. altitude [m] : {A:.0f}")

        time.sleep(60)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
