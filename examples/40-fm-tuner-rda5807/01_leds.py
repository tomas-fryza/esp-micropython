"""
LEDs

Schematic:
  * https://easyeda.com/editor#id=37887f9350854232a235cdf468bfeedc|aad7b1e50d564cfd87c74929a26a139c

Authors:
- Tomas Fryza

Creation date: 2025-05-18
Last modified: 2025-05-19
"""

from machine import Pin
import time

# Set your pins
PIN_LED = 2
PIN_LED_0 = 19
PIN_LED_1 = 18
PIN_LED_2 = 5
PIN_LED_3 = 17

led_builtin = Pin(PIN_LED, Pin.OUT)
led_builtin.on()
led_0 = Pin(PIN_LED_0, Pin.OUT)
led_1 = Pin(PIN_LED_1, Pin.OUT)
led_2 = Pin(PIN_LED_2, Pin.OUT)
led_3 = Pin(PIN_LED_3, Pin.OUT)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led_0.value(not led_0.value())
        time.sleep(0.5)
        led_1.value(not led_1.value())
        time.sleep(0.5)
        led_2.value(not led_2.value())
        time.sleep(0.5)
        led_3.value(not led_3.value())
        time.sleep(0.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_builtin.off()
    led_0.off()
    led_1.off()
    led_2.off()
    led_3.off()
