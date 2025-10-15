"""
Timer-based task management

This script utilizes the ESP32's Timer0 to manage multiple tasks 
periodically. It features three tasks that execute at different
intervals. The timer interrupt updates global counter and flags,
allowing tasks to run based on elapsed time.

Author: Tomas Fryza

Creation date: 2023-10-16
Last modified: 2025-10-15
"""

from machine import Timer
from hw_config import Led

# Global millisecond counter
cnt = 0

# Task run flags (set in interrupt, read in main loop)
flag_a = False
flag_b = False
flag_c = False

# Task periods in milliseconds
period_a = 1000
period_b = 900
period_c = 1100


def task_a():
    print(f"[{cnt}] Task A: LED toggle")
    led.toggle()


def task_b():
    print(f"[{cnt}] Task B")


def task_c():
    print(f"[{cnt}] Task C")


def timer_handler(t):
    """Interrupt handler for Timer runs every 1ms, sets task flags."""
    global cnt, flag_a, flag_b, flag_c
    cnt += 1

    if cnt % period_a == 0:
        flag_a = True
    if cnt % period_b == 0:
        flag_b = True
    if cnt % period_c == 0:
        flag_c = True


def run_tasks():
    global flag_a, flag_b, flag_c
    if flag_a:
        task_a()
        flag_a = False

    if flag_b:
        task_b()
        flag_b = False

    if flag_c:
        task_c()
        flag_c = False


# Start the timer and interrupt every 1 millisecond
tim = Timer(0)
tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

# Create object(s) for LED(s)
led = Led(2)

print("Interrupt-based scheduler running. Press Ctrl+C to stop.")

try:
    # Forever loop
    while True:
        run_tasks()

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    led.off()
