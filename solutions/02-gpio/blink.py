"""
LED blink example

This script blinks an LED connected to the ESP32 board
using a simple forever loop. The LED is toggled on and off
with a short delay. The program can be interrupted using
Ctrl+C.

Components:
- ESP32-based board
- LED connected to GPIO pin 2 (on-board)

Authors:
- Wokwi
- Tomas Fryza

Creation date: 2023-09-21
Last modified: 2024-11-02
"""

# Import the `Pin` class from the `machine` module to access hardware
from machine import Pin
import time

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
