"""
<<<<<<< HEAD
Blink the onboard LED

This MicroPython script controls an on-board LED by repeatedly
switching it on and off. It serves as a simple example of 
how to control an output pin of a microcontroller.

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Run the script
2. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.
=======
LED blink example

This script blinks an LED connected to the ESP32 board
using a simple forever loop. The LED is toggled on and off
with a short delay. The program can be interrupted using
Ctrl+C.

Components:
  - ESP32 microcontroller
  - LED connected to GPIO2 (on-board)
>>>>>>> 0fc769eb19f547d1e95d25b88562e4e2e92cd9b2

Author: Wokwi, Tomas Fryza
Date: 2023-09-21
"""

# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
<<<<<<< HEAD
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
=======
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
        # time.sleep_ms(500)
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped")

    # Optional cleanup code
    led.off()

    # Stop program execution
    sys.exit(0)
>>>>>>> 0fc769eb19f547d1e95d25b88562e4e2e92cd9b2
