"""
Blink three LEDs

This MicroPython script blinks three LEDs connected to the ESP32
microcontroller. The LEDs are controlled individually in a sequence.

Components:
  - ESP32 microcontroller
  - LED0: GPIO pin 2 (onboard)
  - LED1: GPIO pin 25
  - LED2: GPIO pin 26
  - BTN: GPIO pin 27 (optional)

Instructions:
1. Connect LEDs to GPIO pins
2. Run the script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Creation Date: 2023-10-12
Last Modified: 2024-09-27
"""

# Load `Pin` class from `machine` module to access hardware
from machine import Pin
import time
import sys

# Define three LED pins
led0 = Pin(2, Pin.OUT)
led1 = Pin(25, Pin.OUT)
led2 = Pin(26, Pin.OUT)

# Uncomment the following line if you want to use a button
# button = Pin(27, Pin.IN, Pin.PULL_UP)

print(f"Start blinking LEDs: {led0, led1, led2}...")
print("Press `Ctrl+C` to stop")

try:
    # Forever loop
      while True:
        # Turn on the first LED, wait 250 ms, and turn it off
        print(f"LED {led0}")
        led0.on()
        time.sleep(0.25)
        led0.off()
        time.sleep(.25)

        # Repeat the above process for the second LED
        print(f"LED {led1}")
        led1.on()
        time.sleep(0.25)
        led1.off()
        time.sleep(0.25)

        # Repeat the above process for the third LED
        print(f"LED {led2}")
        led2.on()
        time.sleep(0.25)
        led2.off()
        time.sleep(0.25)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led0.off()  # Turn off the LEDs
    led1.off()
    led2.off()

    # Stop program execution
    sys.exit(0)
