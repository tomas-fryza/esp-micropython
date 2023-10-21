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

# Timer interrupt global variable
timer_counter = 0


def irq_timer0(t):
    """Interrupt handler of Timer0"""
    # Get access to the global variable in the function
    global timer_counter
    timer_counter += 1


# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
timer0.init(mode=Timer.PERIODIC, period=100, callback=irq_timer0)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Start counting {timer0}...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        if timer_counter > 20:
            timer_counter = 0
            print("Timer0 interrupt triggered 20 times")

            # You can put a `heavy computing task` here

except KeyboardInterrupt:
    timer0.deinit()  # Deinitialize the timer
    print("Ctrl+C Pressed. Exiting...")
