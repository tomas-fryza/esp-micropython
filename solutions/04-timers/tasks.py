"""
Timer-based task management

This script utilizes the ESP32's Timer0 to manage multiple tasks 
periodically. It features three tasks that execute at different
intervals. The timer interrupt updates global counter and flags,
allowing tasks to run based on elapsed time.

Components:
- ESP32-based board
- LED connected to GPIO pin 2 (on-board)

Author: Tomas Fryza

Creation date: 2023-10-16
Last modified: 2025-10-12
"""

from machine import Timer
from hw_config import Led
import time

# Initialize global counter for different task(s)
cnt = 0

# Task run flags (set in interrupt, read in main loop)
task_a_run = False
task_b_run = False
task_c_run = False

# Task periods in milliseconds
PERIOD_A = 500
PERIOD_B = 500
PERIOD_C = 1100


def timer_handler(t):
    """Interrupt handler for Timer runs every 1ms, sets task flags."""
    global cnt, task_a_run, task_b_run, task_c_run
    cnt += 1

    if cnt % PERIOD_A == 0:
        task_a_run = True
    if cnt % PERIOD_B == 0:
        task_b_run = True
    if cnt % PERIOD_C == 0:
        task_c_run = True


def task_a():
    print(f"[{cnt} ms] Task A: LED toggle")
    led.toggle()


def task_b():
    print(f"[{cnt} ms] Task B")


def task_c():
    print(f"[{cnt} ms] Task C")


# Start the timer and interrupt every 1 millisecond
tim = Timer(0)
tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

# Create object(s) for LED(s)
led = Led(2)

print("Interrupt-based scheduler running. Press Ctrl+C to stop.")

try:
    # Forever loop
    while True:
        if task_a_run:
            task_a()
            task_a_run = False

        if task_b_run:
            task_b()
            task_b_run = False

        if task_c_run:
            task_c()
            task_c_run = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    led.off()
