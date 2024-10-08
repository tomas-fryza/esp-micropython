"""
Example of ESP32 Timer

This script demonstrates how to use a hardware timer
interrupt on the ESP32. A Timer0 interrupt is set up
to trigger every 1000 milliseconds and an interrupt
handler function is called each time the timer period
elapses.

Components:
  - ESP32 microcontroller

Author: Tomas Fryza
Creation Date: 2023-10-16
Last Modified: 2024-09-27
"""

from machine import Timer
import sys


def timer_handler(t):
    """Interrupt handler for Timer0.

    This function is called automatically by the Timer0
    interrupt every time the timer period elapses. The parameter
    `t` is the Timer object that triggered the interrupt.
    """
    print(f"Handler of {t} executed")


# Create an object for 64-bit Timer0
# The ESP32 has 4 hardware timers numbered 0 to 3.
tim = Timer(0)

# Initialize the timer to call the handler every 1000 s
tim.init(period=1000,             # Timer period in milliseconds
         mode=Timer.PERIODIC,     # Set the timer to repeat after each period
         callback=timer_handler)  # Function to call when the timer triggers

print("Timer started. Press `Ctrl+C` to stop")

try:
    # Forever loop to keep the program running
    # The timer runs independently in the background
    while True:
        pass

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer

    # Stop program execution
    sys.exit(0)
