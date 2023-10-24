"""
Button state monitoring

This MicroPython script monitors the state of a button connected
to an ESP32 microcontroller. It detects button presses (active LOW)
and implements a simple debouncing mechanism.

Hardware Configuration:
  - BTN: GPIO pin 27

Instructions:
1. Connect button to GPIO pin
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-12
"""

from machine import Pin
import time

# Define the GPIO pin for the button
button = Pin(27, Pin.IN, Pin.PULL_UP)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Press the button on {button}...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        # Check if the button is pressed (active LOW)
        if button.value() == 0:
            print("Button pressed  ", end="")
            time.sleep_ms(10)  # Delay to debounce the button

            # Wait here until the button is released
            while button.value() == 0:
                pass
            time.sleep_ms(10)  # Additional delay for stability

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
