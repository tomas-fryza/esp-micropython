from machine import Pin
import time

# Define the GPIO pin for the button
button = Pin(26, Pin.IN, Pin.PULL_UP)

while True:
    # Check if the button is pressed (active LOW)
    if button.value() == 0:
        print("X", end="")
        time.sleep_ms(10)

        # Wait here the button is released
        while button.value() == 0:
            pass
        time.sleep_ms(10)
