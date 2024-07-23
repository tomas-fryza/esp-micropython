# ESP32-C3-DevKit-RUST
#   https://github.com/esp-rs/esp-rust-board
#
# Read temperature and humidity from on-board SHTC3 sensor
#   https://sensirion.com/media/documents/643F9C8E/63A5A436/Datasheet_SHTC3.pdf
#
# Inspired by:
#   https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
#   https://github.com/jposada202020/MicroPython_SHTC3/tree/master


from machine import Pin, I2C
import time
import struct
import sys


# SHTC3 sensor
ADDR = 0x70
SLEEP = 0xb098
WAKEUP = 0x3517
NORMAL_MODE = 0x58e0     # Read RH first
LOW_POWER_MODE = 0x401a  # Read RH first

# Status LED
PIN_LED = 7


i2c = I2C(0, scl=Pin(8), sda=Pin(10), freq=400_000)

print("Scanning I2C... ", end="")
devices = i2c.scan()
print(f"{len(devices)} device(s) detected")

for device in devices:
    print(f"{device},\t{hex(device)}")
print("")

if ADDR in devices:
    print(f"Start reading from sensor {hex(ADDR)} @ {i2c}")
    print("Press `Ctrl+C` to stop\n")
else:
    print(f"Sensor {hex(ADDR)} not available")
    print("Program stopped")
    sys.exit(0)


# Status LED
led = Pin(PIN_LED, Pin.OUT)
led.off()

data = bytearray(6)

# Forever loop
try:
    while True:
        led.on()

        i2c.writeto(ADDR, WAKEUP.to_bytes(2, "big"), False)
        time.sleep(0.001)
        i2c.writeto(ADDR, NORMAL_MODE.to_bytes(2, "big"), False)
        time.sleep(0.013)

        i2c.readfrom_into(ADDR, data, False)

        i2c.writeto(ADDR, SLEEP.to_bytes(2, "big"), False)
        time.sleep(0.001)
        led.off()

        humidity = struct.unpack_from(">H", data[0:2])[0]
        humi = (625 * humidity) >> 12
        humi /= 100.0

        temperature = struct.unpack_from(">H", data[3:5])[0]
        temp = ((4375 * temperature) >> 14) - 4500
        temp /= 100.0

        print(f"Temperature: {temp:0.1f} °C\tHumidity: {humi:0.1f} %")

        time.sleep(5)

# Ctrl+C
except KeyboardInterrupt:
    print("Program stopped")

    # Optional cleanup code
    led.off()

    # Stop program execution
    sys.exit(0)
