"""
Blink the onboard LED

This MicroPython script controls an on-board LED by repeatedly
switching it on and off. It serves as a simple example of 
how to control an output pin of a microcontroller.

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Run the current script
2. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Wokwi, Tomas Fryza
Date: 2023-09-21
"""

# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
from time import sleep_ms

# Check the LED pin on your board (usually GPIO 2)
led = Pin(2, Pin.OUT)

print(f"Start blinking {led}...")

# Forever loop
while True:
    led.on()          # Turn on the LED
    sleep_ms(25)      # Sleep for 25 ms
    led.off()         # Turn off the LED
    sleep_ms(975)     # Sleep for 975 ms (total cycle time is 1 sec)
