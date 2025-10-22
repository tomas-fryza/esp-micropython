"""
Timer-based task management

This script utilizes the ESP32's Timer0 to manage multiple tasks 
periodically. The tasks are defined within a dictionary, including
name and period.

Author: Tomas Fryza

Creation date: 2025-10-15
Last modified: 2025-10-15
"""

from machine import Timer
from hw_config import Led

# Global millisecond counter
cnt = 0


def task_a():
    print(f"[{cnt}] Task A: LED toggling")
    led.toggle()


def task_b():
    print(f"[{cnt}] Running task B")


def task_c():
    print(f"[{cnt}] Running task C")


# Task configuration as a list of dictionaries: each with its
# own period (ms), flag, and function name
tasks = [
    {'period': 500,
     'flag': False,
     'func': task_a},
    
    {'period': 1000,
     'flag': False,
     'func': task_b},
    
    {'period': 1500,
     'flag': False,
     'func': task_c},
    ]


def timer_handler(t):
    global cnt, tasks
    cnt += 1
    for task in tasks:
        if cnt % task['period'] == 0:
            task['flag'] = True


def run_tasks():
    global tasks
    for task in tasks:
        if task['flag']:
            task['func']()
            task['flag'] = False


# Setup timer interrupt every 1ms
tim = Timer(0)
tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

led = Led(2)

print("Interrupt-based scheduler running. Press Ctrl+C to stop.")

try:
    while True:
        run_tasks()

except KeyboardInterrupt:
    print("Program stopped. Exiting...")
    tim.deinit()
