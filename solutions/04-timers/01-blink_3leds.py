"""
MicroPython Script for Timer Interrupt and LED Control

This script demonstrates how to use MicroPython on an
ESP32 microcontroller to create a timer interrupt and
control an on-board LED. It configures Timer0 to trigger
an interrupt every 100 milliseconds, toggling the LED state.

Hardware Configuration:
  - LED0: GPIO pin 2 (onboard)
  - LED1: GPIO pin 3
  - LED2: GPIO pin 1

Instructions:
1. Connect LEDs to GPIO pins
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-16
"""

from machine import Pin
from machine import Timer


def irq_timer0(t):
    """Interrupt handler of Timer0"""
    led0.value(not led0.value())


def irq_timer1(t):
    """Interrupt handler of Timer1"""
    led1.value(not led1.value())


def irq_timer2(t):
    """Interrupt handler of Timer2"""
    led2.value(not led2.value())


# Create an object for on-board LED
led0 = Pin(2, mode=Pin.OUT)
# Other LEDs
led1 = Pin(3, mode=Pin.OUT)
led2 = Pin(1, mode=Pin.OUT)

# Create an object for 64-bit Timer0
timer0 = Timer(0)  # Between 0-3 for ESP32
# Init the Timer and call the interrupt handler every 100 ms
timer0.init(mode=Timer.PERIODIC, period=100, callback=irq_timer0)

# Other Timers
timer1 = Timer(1)
timer1.init(mode=Timer.PERIODIC, period=200, callback=irq_timer1)

timer2 = Timer(2)
timer2.init(mode=Timer.PERIODIC, period=500, callback=irq_timer2)
