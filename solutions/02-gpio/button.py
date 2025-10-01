"""
Button state monitoring

This MicroPython script monitors the state of a button connected
to an ESP32 microcontroller. It detects button presses (active LOW)
and implements a simple debouncing mechanism.

Components:
- ESP32-based board
- Button connected to GPIO pin 27

Author: Tomas Fryza

Creation date: 2023-10-12
Last modified: 2025-10-01
"""

from machine import Pin
import time

# Define the GPIO pin for the button
btn = Pin(27, Pin.IN, Pin.PULL_UP)

print(f"Press the button on {btn}...")
print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Check if the button is pressed (active LOW)
        if btn.value() == 0:
            print("Button pressed")
            time.sleep(0.01)  # Short delay to debounce the button

            # Wait here until the button is released
            while btn.value() == 0:
                pass
            time.sleep(0.01)  # Additional delay for stability

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
