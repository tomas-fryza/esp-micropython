"""
Blink the On-Board LED

This MicroPython script controls an on-board LED by repeatedly
switching it on and off. It serves as a simple example of 
how to control an output pin of a microcontroller.

Inspired by:
    - https://wokwi.com/projects/359801682833812481

Author: Tomas Fryza
Date: 2023-09-21
"""
# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
from time import sleep_ms

# Check the LED pin on your board (usually GPIO2)
print("Configure output pin #2... ", end="")
led = Pin(2, Pin.OUT)
print("Done")
print("Start blinking...")

# Forever loop
while True:
    led.on()          # Turn on the LED
    sleep_ms(25)      # Sleep for 25 ms
    led.off()         # Turn off the LED
    sleep_ms(975)     # Sleep for 975 ms (total cycle time is 1 second)
