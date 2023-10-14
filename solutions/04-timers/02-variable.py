"""
Here is a Python script that increments a variable each time
the timer triggers an interrupt. In the main loop, when the variable
is 10, a specific task is performed.
"""

from machine import Timer, Pin

timer_0 = Timer(0)  # Between 0-3 for ESP32
timer_count = 0     # global variable


def interruption_handler(pin):
    global timer_count
    timer_count += 1


if __name__ == "__main__":
    timer_count_old = 0
    timer_0.init(mode=Timer.PERIODIC, period=100, callback=interruption_handler)

    while True:
        if timer_count > 10:
            timer_count = 0
            print("10x")
            # heavy task here
