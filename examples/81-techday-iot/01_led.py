"""
Onboard LED blink
"""

from machine import Pin
from time import sleep_ms

led = Pin(2, Pin.OUT)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led.on()
        sleep_ms(100)
        led.off()
        sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
