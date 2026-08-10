"""
Blink three LEDs

Components:
- Raspberry Pi Pico + LAFVIN board
- LED: WL_GPIO0 (onboard)
- LED1: GPIO pin 16
- LED2: GPIO pin 17

Authors:
- Tomas Fryza

Creation date: 2023-10-12
Last modified: 2026-07-21
"""

from machine import Pin
from time import sleep_ms

led = Pin("LED", Pin.OUT)  # Or "WL_GPIO0", "EXT_GPIO0"
led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)

print("Press `Ctrl+C` to stop")
print()

try:
    # Forever loop
    while True:
        led.on()
        print(f"{led}")
        sleep_ms(100)
        led.off()
        sleep_ms(900)

        led1.on()
        print(f"{led1}")
        sleep_ms(100)
        led1.off()
        sleep_ms(900)

        led2.on()
        print(f"{led2}")
        sleep_ms(100)
        led2.off()
        sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led.off()
    led1.off()
    led2.off()
