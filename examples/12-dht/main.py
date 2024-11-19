#
# See:
# https://docs.micropython.org/en/latest/esp8266/tutorial/dht.html
#

from machine import Pin
import dht

my_dht = dht.DHT22(Pin(18, Pin.IN, Pin.PULL_UP))

my_dht.measure()
print(f"{my_dht.temperature()} °C")
print(f"{my_dht.humidity()} %")
