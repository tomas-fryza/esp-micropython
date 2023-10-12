"""
Button State Monitoring

This MicroPython script monitors the state of a button connected
to an ESP32 microcontroller. It detects button presses (active LOW)
and implements a simple debouncing mechanism.

Hardware Configuration:
- Connect a button to GPIO Pin 26.
- Ensure the button has an external pull-up resistor or use Pin.PULL_UP.

Author: Tomas Fryza
Date: 2023-10-12
"""

from machine import Pin
import time

# Define the GPIO pin for the button
button = Pin(26, Pin.IN, Pin.PULL_UP)

while True:
    # Check if the button is pressed (active LOW)
    if button.value() == 0:
        print("Button Pressed", end="")
        time.sleep_ms(10)  # Delay to debounce the button

        # Wait here until the button is released
        while button.value() == 0:
            pass
        time.sleep_ms(10)  # Additional delay for stability
