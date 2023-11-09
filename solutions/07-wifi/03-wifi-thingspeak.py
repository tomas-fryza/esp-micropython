from machine import Pin, I2C
import network
import urequests  # Network Request Module
from time import sleep


def connect_wifi():
    from time import sleep_ms

    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PSWD)
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")


def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


def read_dht12_sensor():
    # Read 5 bytes from addr. 0 from peripheral with 7-bit address 0x5c
    led.on()
    i2c.readfrom_mem_into(0x5c, 0, buf)
    led.off()

    # Check the checksum
    if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
        raise Exception("Checksum error")


# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
THINGSPEAK_API_KEY = "<THINGSPEAK WRITE API KEY>"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

# Create I2C peripheral at frequency of 400 kHz
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

# Status LED
led = Pin(2, Pin.OUT)

# Create an array of 5 bytes (2x humidity, 2x temperature, 1x checksum)
buf = bytearray(5)

# Forever loop
while True:
    read_dht12_sensor()

    # Put data together
    humi = buf[0] + (buf[1]*0.1)
    temp = buf[2] + (buf[3]*0.1)
    print(f"Temperature: {temp} C\tHumidity: {humi} %")

    connect_wifi()

    # Send data using a POST request
    request = urequests.post(
        'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_API_KEY,
        json={"field1": temp, "field2": humi},
        headers={"Content-Type": "application/json"})
    print(f"Request #{request.text} sent")
    request.close()

    disconnect_wifi()

    # Put device to sleep for 60 seconds
    sleep(60)
