"""
Blink the onboard LED

This MicroPython script controls an on-board LED by repeatedly
switching it on and off. It serves as a simple example of 
how to control an output pin of a microcontroller.

Components:
- ESP32-based board
- LED connected to GPIO2 (on-board)

Instructions:
1. Run the script
2. Stop the code execution by pressing `Ctrl+C` key

Authors:
- Wokwi
- Tomas Fryza

Creation date: 2023-06-12
Last modified: 2024-11-02
"""

# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
import time

# Initialize LED pin (e.g., GPIO2 for ESP32 board)
led = Pin(2, Pin.OUT)

print(f"Start blinking {led}. Press `Ctrl+C` to stop")

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
