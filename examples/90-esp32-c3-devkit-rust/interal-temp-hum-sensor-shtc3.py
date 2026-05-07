# ESP32-C3-DevKit-RUST
#   https://github.com/esp-rs/esp-rust-board
#
# Datasheet of temperature and humidity on-board SHTC3 sensor
#   https://sensirion.com/media/documents/643F9C8E/63A5A436/Datasheet_SHTC3.pdf
#
# Inspired by:
#   https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
#   https://github.com/jposada202020/MicroPython_SHTC3/tree/master


from machine import Pin, I2C
import time

from shtc3 import SHTC3

# Used pins for ESP32-C3-DevKit-RUST
PIN_LED = 7
PIN_SCL = 8
PIN_SDA = 10

i2c = I2C(0, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=100_000)
led = Pin(PIN_LED, Pin.OUT)
led.off()
sensor = SHTC3(i2c)

print("Scanning I2C... ", end="")
devices = i2c.scan()
print(f"{len(devices)} device(s) detected")
for device in devices:
    print(f"{device},\t{hex(device)}")
print()

print(f"I2C configuration : {str(i2c)}")
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        led.on()

        try:
            temp, hum = sensor.read()
            print(f"Temperature: {temp:.2f} °C  Humidity: {hum:.2f} %")
        except RuntimeError as e:
            print("Sensor error:", e)

        led.off()
        time.sleep(5)

except KeyboardInterrupt:
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
