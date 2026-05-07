from machine import Pin, I2C
import time
import network
import wifi_utils
import config
import urequests

from shtc3 import SHTC3
from sh1106 import SH1106_I2C


def send_to_thingspeak(temp, humidity):
    """
    Send temperature and humidity data to ThingSpeak.

    :param float temp: The temperature value to send.
    :param float humidity: The humidity value to send.
    """
    API_URL = "https://api.thingspeak.com/update"

    # Select GET or POST request
    # Make the GET request
    url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={humidity}"
    response = urequests.get(url)

    # Make the POST request
    # url = f"{API_URL}?api_key={API_KEY}"
    # payload = {"field1": temp, "field2": humidity}
    # headers = {"Content-Type": "application/json"}
    # response = urequests.post(url, json=payload, headers=headers)

    print(f"ThingSpeak entry no.: {response.text}")
    response.close()


# Used pins for ESP32-C3-DevKit-RUST
PIN_LED = 7
PIN_SCL = 8
PIN_SDA = 10

API_KEY = "IL5UY2KVNASJBQMU"

# Init SHTC3 sensor
i2c = I2C(0, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=100_000)
sensor = SHTC3(i2c)

# Init OLED display
display = SH1106_I2C(i2c)
display.contrast(50)  # Set contrast to 50 %
display.text(" T[C]  H[%]", 40, 0)
display.text("Min:", 0, 40)
display.text("Max:", 0, 50)

# Status LED
led = Pin(PIN_LED, Pin.OUT)
led.off()

# Create Station interface
wifi = network.WLAN(network.STA_IF)

temp_min = 100
temp_max = -100
hum_min = 100
hum_max = 0

print(f"I2C configuration : {str(i2c)}")
print("Press `Ctrl+C` to stop")
print()

try:
    while True:
        led.on()

        try:
            temp, hum = sensor.read()
            if temp < temp_min:
                    temp_min = temp
            if temp > temp_max:
                    temp_max = temp
            if hum < hum_min:
                    hum_min = hum
            if hum > hum_max:
                    hum_max = hum

            print(f"Temperature: {temp:6.2f} °C  Humidity: {hum:5.2f} %")

            display.fill_rect(40, 20, 120, 50, 0)
            display.text(f"{temp:5.1f}  {hum:4.1f}", 40, 20)
            display.text(f"{temp_min:5.1f}  {hum_min:4.1f}", 40, 40)
            display.text(f"{temp_max:5.1f}  {hum_max:4.1f}", 40, 50)
            display.show()

            wifi_utils.connect(wifi, config.SSID, config.PSWD)
            send_to_thingspeak(temp, hum)
            wifi_utils.disconnect(wifi)

        except RuntimeError as e:
            print("Sensor error:", e)

        led.off()
        time.sleep(60)

except KeyboardInterrupt:
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
    display.poweroff()
    wifi_utils.disconnect(wifi)
