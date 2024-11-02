"""
Blink three LEDs

This MicroPython script blinks three LEDs connected to the ESP32
microcontroller. The LEDs are controlled individually in a sequence.

Components:
- ESP32-based board
- LED0: GPIO pin 2 (onboard)
- LED1: GPIO pin 25
- LED2: GPIO pin 26
- BTN: GPIO pin 27 (optional)

Author: Tomas Fryza

Creation date: 2023-10-12
Last modified: 2024-11-02
"""

# Load `Pin` class from `machine` module to access hardware
from machine import Pin
import time

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
    led0.off()
    led1.off()
    led2.off()
