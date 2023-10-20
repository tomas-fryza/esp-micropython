"""
MicroPython Script for Timer Interrupt and LED Control

This script demonstrates how to use MicroPython on an
ESP32 microcontroller to create a timer interrupt and
control an on-board LED. It configures Timer0 to trigger
an interrupt every 100 milliseconds, toggling the LED state.

Dependencies:
- MicroPython machine library
- MicroPython Timer module

Instructions:
1. Flash this script to your ESP32 microcontroller.
2. Connect an LED to GPIO pin 2.
3. The LED will toggle its state every 100 milliseconds due to the timer interrupt.

Author: Tomas Fryza
Date: 2023-10-16
"""

from machine import Pin
from machine import Timer
from time import sleep_ms


def irq_handler0(t):
    """Interrupt handler of Timer0"""
    led0.value(not led0.value())


def irq_handler1(t):
    """Interrupt handler of Timer1"""
    led1.value(not led1.value())


def irq_handler2(t):
    """Interrupt handler of Timer2"""
    led2.value(not led2.value())


# Create an object for on-board LED
led0 = Pin(2, mode=Pin.OUT)
led1 = Pin(1, mode=Pin.OUT)
led2 = Pin(3, mode=Pin.OUT)

# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
# Init the Timer and call the handler every 100 ms
timer0.init(
    mode=Timer.PERIODIC,
    period=500,
    callback=irq_handler0)

# Other Timers
timer1 = Timer(1)
timer1.init(
    mode=Timer.PERIODIC,
    period=200,
    callback=irq_handler1)

timer2 = Timer(2)
timer2.init(
    mode=Timer.PERIODIC,
    period=100,
    callback=irq_handler2)


while True:
    sleep_ms(5)
