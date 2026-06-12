"""
Onboard LED blink

See datasheet:
https://admin.techshopbd.com/uploads/product_document/Raspberry_Pico_W_Datasheet.pdf

"""

from machine import Pin
from time import sleep_ms

led = Pin("LED", Pin.OUT)  # Or "WL_GPIO0"

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led.on()
        print(".", end="")
        sleep_ms(100)
        led.off()
        sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led.off()

