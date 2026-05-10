"""
LEDs

Authors:
- Tomas Fryza
- https://easyeda.com/editor#id=4e272acacecf42169229b9288f3defe5|5251c125583f4b4985e5f40a20381136

Creation date: 2025-05-18
Last modified: 2026-05-10
"""

from machine import Pin
import time

# Set your pins
PIN_LED = 2
PIN_LED_0 = 19
PIN_LED_1 = 18
PIN_LED_2 = 5

led = Pin(PIN_LED, Pin.OUT)
led.on()
led_0 = Pin(PIN_LED_0, Pin.OUT)
led_1 = Pin(PIN_LED_1, Pin.OUT)
led_2 = Pin(PIN_LED_2, Pin.OUT)

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

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
    led_0.off()
    led_1.off()
    led_2.off()
