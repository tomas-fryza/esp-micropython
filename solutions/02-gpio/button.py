"""
Button state monitoring

This MicroPython script monitors the state of a button connected
to an ESP32 microcontroller. It detects button presses (active LOW)
and implements a simple debouncing mechanism.

Components:
  - ESP32 microcontroller
  - Button connected to GPIO pin 27

Instructions:
1. Connect button to GPIO pin
2. Run the script
3. Stop the code execution by pressing `Ctrl+C` key

Author: Tomas Fryza
Creation Date: 2023-10-12
Last Modified: 2024-09-27
"""

from machine import Pin
import time
import sys

# Define the GPIO pin for the button
button = Pin(27, Pin.IN, Pin.PULL_UP)

print(f"Press the button on {button}...")
print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Check if the button is pressed (active LOW)
        if button.value() == 0:
            print("Button pressed")
            time.sleep(0.01)  # Short delay to debounce the button

            # Wait here until the button is released
            while button.value() == 0:
                pass
            time.sleep(0.01)  # Additional delay for stability

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
