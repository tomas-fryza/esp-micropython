#
# See:
# https://docs.micropython.org/en/latest/esp8266/tutorial/dht.html
#

from machine import Pin
import dht

my_dht = dht.DHT22(Pin(17, Pin.IN, Pin.PULL_UP))

my_dht.measure()
print(f"Temperature: {my_dht.temperature()} °C")
print(f"Humidity: {my_dht.humidity()} %")
