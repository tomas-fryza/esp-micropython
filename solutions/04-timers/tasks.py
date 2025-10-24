"""
Timer-based task management

This script utilizes the ESP32's Timer0 to manage multiple tasks 
periodically. The tasks are defined within a dictionary, including
name and period.

Author: Tomas Fryza

Creation date: 2023-10-16
Last modified: 2025-10-24
"""

from machine import Timer
from hw_config import Led

tick_ms = 0

led = Led(2)


def task_a():
    print(f"[{tick_ms}] Task A: LED toggle")
    led.toggle()


def task_b():
    print(f"[{tick_ms}] Task B")


def task_c():
    print(f"[{tick_ms}] Task C")


# Define all periodic tasks in one table
tasks = [
    {"func": task_a, "period": 500, "flag": False},
    {"func": task_b, "period": 250, "flag": False},
    {"func": task_c, "period": 750, "flag": False},
]


def timer_handler(t):
    """Interrupt handler for Timer runs every 1ms, sets task flags."""
    global tick_ms
    tick_ms += 1

    for task in tasks:
        if tick_ms % task["period"] == 0:
            task["flag"] = True


# 1 ms base tick for the whole system
Timer(0).init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

print("Interrupt-based scheduler running. Press Ctrl+C to stop.")
try:
    # Forever loop
    while True:
        for task in tasks:
            if task["flag"]:
                task["func"]()
                task["flag"] = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
