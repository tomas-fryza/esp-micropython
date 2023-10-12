"""Blink three off-board LEDs
"""

# Load `Pin` class from `machine` module in order to access the hardware
from machine import Pin
from time import sleep_ms

led0 = Pin(3, Pin.OUT)
led1 = Pin(1, Pin.OUT)
led2 = Pin(25, Pin.OUT)

# button = Pin(26, Pin.IN, Pin.PULL_UP)

# Forever loop
while True:
    led0.on()
    sleep_ms(250)
    led0.off()
    sleep_ms(250)

    led1.on()
    sleep_ms(250)
    led1.off()
    sleep_ms(250)

    led2.on()
    sleep_ms(250)
    led2.off()
    sleep_ms(250)
