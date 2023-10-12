"""
Blink Three Off-Board LEDs

This MicroPython script blinks three off-board LEDs connected
to the ESP32 microcontroller. The LEDs are controlled individually
in a sequence.
- LED0 is connected to GPIO Pin 3.
- LED1 is connected to GPIO Pin 1.
- LED2 is connected to GPIO Pin 25.

Replace the GPIO pin numbers with the actual pin connections on your hardware.

Author: Tomas Fryza
Date: 2023-10-12
"""

# Load `Pin` class from `machine` module to access hardware
from machine import Pin
from time import sleep_ms

# Define three LED pins (replace with actual GPIO pin numbers)
led0 = Pin(3, Pin.OUT)
led1 = Pin(1, Pin.OUT)
led2 = Pin(25, Pin.OUT)

# Uncomment the following line if you want to use a button
# button = Pin(26, Pin.IN, Pin.PULL_UP)

# Forever loop
while True:
    # Turn on the first LED, wait 250 ms, and turn it off
    led0.on()
    sleep_ms(250)
    led0.off()
    sleep_ms(250)

    # Repeat the above process for the second LED
    led1.on()
    sleep_ms(250)
    led1.off()
    sleep_ms(250)

    # Repeat the above process for the third LED
    led2.on()
    sleep_ms(250)
    led2.off()
    sleep_ms(250)
