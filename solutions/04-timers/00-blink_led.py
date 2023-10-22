"""
MicroPython Script for Timer Interrupt and LED Control

This script demonstrates how to use MicroPython on an
ESP32 microcontroller to create a timer interrupt and
control an on-board LED. It configures Timer0 to trigger
an interrupt every 100 milliseconds, toggling the LED state.

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Use onboard LED or connect an external
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-16
"""

from machine import Pin
from machine import Timer


def timer0_handler(t):
    """Interrupt handler of Timer0"""
    led0.value(not led0.value())


# Create an object for on-board LED
led0 = Pin(2, mode=Pin.OUT)

# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
# Init the Timer and call the handler every 100 ms
timer0.init(mode=Timer.PERIODIC, period=250, callback=timer0_handler)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Start blinking LED {led0}...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        # print("Running...")
        # time.sleep(0.1)
        pass

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
finally:
    # Optional cleanup code
    timer0.deinit()  # Deinitialize the timer
    led0.off()  # Turn off the LED
