# Complete project details at https://RandomNerdTutorials.com/micropython-programming-with-esp32-and-esp8266/

from machine import Pin
from machine import ADC
import time

sensor = ADC(Pin(36))  # A0/36 on FireBeetle v2 board
sensor.atten(ADC.ATTN_11DB)  # Full range: 3.3V

while True:
    value = sensor.read()
    print(value)
    time.sleep_ms(250)
