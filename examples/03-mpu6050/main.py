# https://microcontrollerslab.com/micropython-mpu-6050-esp32-esp8266/

from machine import I2C
from machine import Pin
import time
import mpu6050

# Connect the MPU6050 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
mpu = mpu6050.MPU6050(i2c)

# Ignore the first measurement
mpu.get_raw_values()
time.sleep(1)

print(f"I2C configuration: {str(i2c)}")
print()
print("Start measuring. Press `Ctrl+C` to stop")

try:
    while True:
        mpu.get_values()
        print(mpu.get_values())
        print()

        time.sleep(10)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
