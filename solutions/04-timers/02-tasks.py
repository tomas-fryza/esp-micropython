"""
???

Components:
  - ESP32 microcontroller

Author: Tomas Fryza
Creation Date: 2023-10-16
Last Modified: 2024-09-27
"""

from machine import Pin
from machine import Timer
import sys

# Initialize counters for different tasks
task_a_counter = 0
task_b_counter = 0
task_c_counter = 0

# Define the intervals in terms of timer ticks (e.g., ticks every 100ms)
task_a_interval = 5   # Task A runs every 500ms (5 ticks)
task_b_interval = 10  # Task B runs every 1s (10 ticks)
task_c_interval = 20  # Task C runs every 2s (20 ticks)


def timer_handler(t):
    """Interrupt handler for Timer0."""
    global task_a_counter, task_b_counter, task_c_counter

    # Increment counters
    task_a_counter += 1
    task_b_counter += 1
    task_c_counter += 1


def task_a():
    """Task A: Runs every 100ms"""
    print("Task A executed: LED")
    led.value(not led.value())


def task_b():
    """Task B: Runs every 200ms"""
    print("Task B executed")


def task_c():
    """Task C: Runs every 500ms"""
    print("Task C executed")


# Create and initialize Timer0
tim = Timer(0)
tim.init(period=100,
         mode=Timer.PERIODIC,
         callback=timer_handler)

# Create object for LED
led = Pin(2, mode=Pin.OUT)

print("Timer started. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Task A (every 100ms)
        if task_a_counter >= task_a_interval:
            task_a_counter = 0  # Reset the counter
            task_a()

        # Task B (every 200ms)
        if task_b_counter >= task_b_interval:
            task_b_counter = 0  # Reset the counter
            task_b()

        # Task C (every 500ms)
        if task_c_counter >= task_c_interval:
            task_c_counter = 0  # Reset the counter
            task_c()

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    led.off()

    # Stop program execution
    sys.exit(0)
