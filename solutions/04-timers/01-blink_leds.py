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


def interrupt_handler0(t):
    """Interrupt handler of Timer0"""
    pin_led0.value(not pin_led0.value())


# Create an object for on-board LED
pin_led0 = Pin(2, mode=Pin.OUT)

# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
# Init the Timer and call the handler every 100 ms
timer0.init(
    mode=Timer.PERIODIC,
    period=100,
    callback=interrupt_handler0)
