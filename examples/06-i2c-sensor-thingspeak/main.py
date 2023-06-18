"""Send I2C sensor data to ThingSpeak cloud.

Read data from DHT12 humidity & temperature I2C sensor, and send them
to ThingSpeak.com server via Wi-Fi.

See also:
    https://microcontrollerslab.com/esp32-micropython-bme280-sensor-thingspeak/
"""


import network
from machine import Pin, I2C
import urequests 
from time import sleep


def connect():
    from time import sleep_ms

    if not sta_if.isconnected():
        print("Connecting to network...")

        # Activate station/Wi-Fi client interface
        sta_if.active(True)

        # Connect
        sta_if.connect(YOUR_WIFI_SSID, YOUR_WIFI_PSWD)

        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            sleep_ms(250)


def disconnect():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


def dht_get_values():
    # Read 5 bytes from addr. 0 from peripheral with 7-bit address 0x5c
    led.on()
    i2c.readfrom_mem_into(0x5c, 0, buf)
    led.off()

    # Checksum
    if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
        raise Exception("checksum error")


YOUR_WIFI_SSID = "ssid"
YOUR_WIFI_PSWD = "pswd"
THINGSPEAK_WRITE_API_KEY = "api_key"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

# Create I2C peripheral at frequency of 400kHz
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

led = Pin(2, Pin.OUT)

# Create an array of 5 bytes (2x humidity, 2x temperature, 1x checksum)
buf = bytearray(5)

# Forever loop
while True:
    connect()
    dht_get_values()

    # Display data
    humi = buf[0] + (buf[1]*0.1)
    temp = buf[2] + (buf[3]*0.1)
    print(f"Temperature: {temp} C\tHumidity: {humi} %")

    # Send data
    request = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY,
                             json={"field1":temp, "field2":humi},
                             headers={"Content-Type": "application/json"})
    request.close()
    disconnect()

    # Delay 30 seconds
    sleep(30)
