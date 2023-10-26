"""
The MicroPython script demonstrates the use of a timer interrupt
(specifically Timer0) on an ESP32 microcontroller. Additionally, it
introduces a simple mechanism to count the number of times the timer
interrupt occurs and execute a "heavy task" when the interrupt count
exceeds a certain threshold.

Instructions:
1. Run the script
2. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-16
"""

from machine import Timer

# Define global variable
timer0_counter = 0


def timer0_handler(t):
    """Interrupt handler of Timer0"""
    global timer0_counter  # Access the global timer0_counter
    timer0_counter += 1


# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
timer0.init(period=100, mode=Timer.PERIODIC, callback=timer0_handler)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Start counting {timer0}...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        if timer0_counter > 20:
            timer0_counter = 0
            print("Timer0 interrupt triggered 20 times")

            # You can put a `heavy computing task` here

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")

    # Optional cleanup code
    timer0.deinit()  # Deinitialize the timer
