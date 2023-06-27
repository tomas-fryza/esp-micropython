"""Interruption of four internal Timers.

ESP32 has four 64-bit hardware timers (Timer0, Timer1, Timer2,
and Timer3) based on 16-bit pre-scalers. Init all timers and
wait for interrupt signals.

Inspired by:
    * https://www.upesy.com/blogs/tutorials/timer-esp32-with-micro-python-scripts#
    * https://microcontrollerslab.com/micropython-timers-esp32-esp8266-generate-delay/
"""

from machine import Timer
from machine import Pin


def toggleLed(t):
    led.value(not led.value())


def handleInterrupt(t):
    global counter
    counter += 1
    print(f"Timer1 interrupted {counter} time(s)")


led = Pin(2, Pin.OUT)
counter = 0  # Global variable

# Create a timer object
tim0 = Timer(0)
# Periodically invert LED value 5 times per second
tim0.init(mode=Timer.PERIODIC, freq=5, callback=toggleLed)
# Init function has three parameters:
#   -- mode: PERIODIC (periodically) or ONE_SHOT (once)
#   -- period or freq: Period in ms of frequency in Hz
#   -- callback: Interrupt routine when timer is triggered
print("Timer 0 set to `PERIODIC, freq=5 Hz`")

# Periodically call function every two seconds
tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC, freq=.5, callback=handleInterrupt)
print("Timer 1 set to `PERIODIC, freq=1/2 Hz`")

# Print info just ones after 5_000 millisecs
tim2 = Timer(2)
tim2.init(mode=Timer.ONE_SHOT, period=5000, callback=lambda t:print(f"{t} callback"))
# A lambda function is defined without a name and evaluates and
# returns only one expression.
# Syntax
#   lambda param(s): expression
#   -- lambda: analog of `def` in normal functions
#   -- param(s): argument(s) just like normal function
#   -- expression: code being executed, ideally a single-line
print("Timer 2 set to `ONE_SHOT, period=5_000 ms`")

# Stop and disable Timer1 peripheral after 10 secs
tim3 = Timer(3)
tim3.init(mode=Timer.ONE_SHOT, period=10000, callback=lambda t:tim1.deinit())
print("Timer 3 set to `ONE_SHOT, period=10_000 ms`")
