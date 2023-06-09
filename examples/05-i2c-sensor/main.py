"""Read temperature and humidity via I2C bus.

Use hardware I2C bus and read temperature and humidity values
from DHT12 sensor with SLA = 0x5c (92).

NOTES:
    * Connect DHT12 sensor to I2C pins:

        DHT12  ESP32 ESP8266 ESP32-CAM ESP32C3
        SCL     22      5       15        8
        SDA     21      4       13       10
        +      3.3V    3.3V    3.3V     3.3V
        -      GND     GND     GND      GND

Inspired by:
    * https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
    * https://github.com/mcauser/micropython-dht12/blob/master/dht12.py
"""

from machine import Pin, I2C
from time import sleep

# Status LED at GPIO2
led = Pin(2, Pin.OUT)
led.off()

# Create I2C peripheral at frequency of 100 kHz
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Scan for peripherals, returning a list of 7-bit addresses
# between 0x08 and 0x77 inclusive
print("Scanning for I2C devices... ", end="")
devices = i2c.scan()
device_count = len(devices)

if device_count == 0:
    print("No I2C devices found")
else:
    print(f"{device_count} found")
    for device in devices:
        print(f"Dec address: {device},\tHex address: {hex(device)}")
print("")

# Create an array of 5 bytes
buf = bytearray(5)
# 0 - Humidity integer part
# 1 - Humidity decimal part
# 2 - Temperature integer part
# 3 - Temperature decimal part
# 4 - Checksum

# Forever loop
while True:
    # Read values from device with 7-bit address `0x5c`
    if 0x5c in devices:
        # Read 5 bytes from addr. 0 into `buf` array
        led.on()
        i2c.readfrom_mem_into(0x5c, 0, buf)
        led.off()

        # Test checksum of received data
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception("checksum error")

        # Display data
        humi = buf[0] + (buf[1]*0.1)
        temp = buf[2] + (buf[3]*0.1)
        print(f"Temperature: {temp} C\tHumidity: {humi} %")

    # Delay 5 seconds
    sleep(5)
