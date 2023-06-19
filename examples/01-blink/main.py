"""Blink the on-board LED.

A simple example of how to control one output pin of 
a microcontroller. An LED is connected to the GPIO pin,
which is repeatedly switched on and off.

Inspired by:
    * https://wokwi.com/projects/359801682833812481
"""

from machine import Pin
from time import sleep_ms

# Check the LED pin on your board, usually it is GPIO2
print("Configure output pin... ", end="")
led = Pin(2, Pin.OUT)
print("Done")

# Forever loop
while True:
    led.on()
    sleep_ms(125)
    led.off()
    sleep_ms(875)
