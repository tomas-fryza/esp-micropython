"""
Blink three LEDs

This MicroPython script blinks three LEDs connected to the ESP32
microcontroller. The LEDs are controlled individually in a sequence.

Hardware Configuration:
  - LED0: GPIO pin 2 (onboard)
  - LED1: GPIO pin 25
  - LED2: GPIO pin 26
  - BTN: GPIO pin 27 (optional)

Instructions:
1. Connect LEDs to GPIO pins
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-12
"""

# Load `Pin` class from `machine` module to access hardware
from machine import Pin
from utime import sleep_ms

# Define three LED pins
led0 = Pin(2, Pin.OUT)
led1 = Pin(25, Pin.OUT)
led2 = Pin(26, Pin.OUT)

# Uncomment the following line if you want to use a button
# button = Pin(27, Pin.IN, Pin.PULL_UP)

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        # Turn on the first LED, wait 250 ms, and turn it off
        print(f"LED {led0}")
        led0.on()
        sleep_ms(250)
        led0.off()
        sleep_ms(250)

        # Repeat the above process for the second LED
        print(f"LED {led1}")
        led1.on()
        sleep_ms(250)
        led1.off()
        sleep_ms(250)

        # Repeat the above process for the third LED
        print(f"LED {led2}")
        led2.on()
        sleep_ms(250)
        led2.off()
        sleep_ms(250)
except KeyboardInterrupt:
    led0.off()
    led1.off()
    led2.off()
    print("Ctrl+C Pressed. Exiting...")
