"""
Onboard LED blink
"""

from machine import Pin
import time

led = Pin(2, Pin.OUT)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
