"""
Timer-based task management

This script utilizes the ESP32's Timer0 to manage multiple tasks 
periodically. It features three tasks that execute at different
intervals. The timer interrupt updates global counters, allowing
tasks to run based on elapsed time.

Components:
- ESP32-based board
- LED connected to GPIO pin 2 (on-board)
- Two external LEDs connected to GPIO pin 25 and 26

Author: Tomas Fryza

Creation date: 2023-10-16
Last modified: 2024-11-02
"""

from machine import Timer
from hw_config import Led

# Initialize global counter(s) for different task(s)
counter_a = 0
counter_b = 0
counter_c = 0


def timer_handler(t):
    """Interrupt handler for Timer runs every 1 millisecond."""
    global counter_a, counter_b, counter_c

    # Increment counter(s)
    counter_a += 1
    counter_b += 1
    counter_c += 1


def task_a():
    print(f"Task A executed: onboard LED at {led_onboard}")
    led_onboard.toggle()


def task_b():
    print("Task B executed")


def task_c():
    print("Task C executed")


# Create and initialize the timer
tim = Timer(0)
tim.init(period=1,  # 1 millisecond
         mode=Timer.PERIODIC,
         callback=timer_handler)

# Create object(s) for LED(s)
led_onboard = Led(2)

print("Timer started. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Task A (every 500ms)
        if counter_a >= 500:
            counter_a = 0  # Reset the counter
            task_a()  # Run the task

        # Task B (every 700ms)
        if counter_b >= 700:
            counter_b = 0
            task_b()

        # Task C (every 1,100ms)
        if counter_c >= 1100:
            counter_c = 0
            task_c()

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    led_onboard.off()
