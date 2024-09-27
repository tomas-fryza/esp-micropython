"""
Blink the onboard LED

This MicroPython script controls an on-board LED by repeatedly
switching it on and off. It serves as a simple example of 
how to control an output pin of a microcontroller.

Components:
  - ESP32 microcontroller
  - LED connected to GPIO2 (on-board)

Instructions:
1. Run the current script
2. Stop the code execution by pressing `Ctrl+C` key

Author: Wokwi, Tomas Fryza
Creation Date: 2023-06-12
Last Modified: 2024-09-27
"""

# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
import time
import sys

# Initialize LED pin (e.g., GPIO2 for ESP32 board)
led = Pin(2, Pin.OUT)

print(f"Start blinking {led}")
print("Press `Ctrl+C` to stop")

try:
    # Forever loop to blink the LED
    while True:
        # led.value(not led.value())
        # time.sleep(0.5)
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.9)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()

    # Stop program execution
    sys.exit(0)
