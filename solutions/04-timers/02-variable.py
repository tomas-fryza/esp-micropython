"""
The MicroPython script demonstrates the use of a timer interrupt
(specifically Timer0) on an ESP32 microcontroller. Additionally, it
introduces a simple mechanism to count the number of times the timer
interrupt occurs and execute a "heavy task" when the interrupt count
exceeds a certain threshold.

Instructions:
1. Run the current script
2. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-16
"""

from machine import Timer

n_of_tim0_callbacks = 0  # Make a global variable


def irq_timer0(t):
    """Interrupt handler of Timer0"""
    # Get access to the global variable in the function
    global n_of_tim0_callbacks
    n_of_tim0_callbacks += 1


# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
timer0.init(mode=Timer.PERIODIC, period=100, callback=irq_timer0)

while True:
    if n_of_tim0_callbacks > 10:
        n_of_tim0_callbacks = 0
        print("Timer0 interrupt triggered 10 times")
        # Put a `heavy task` here
