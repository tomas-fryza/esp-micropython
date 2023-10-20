"""
MicroPython Script for Timer Interrupt and LED Control

This script demonstrates how to use MicroPython on an
ESP32 microcontroller to create a timer interrupt and
control an on-board LED. It configures Timer0 to trigger
an interrupt every 100 milliseconds, toggling the LED state.

Hardware Configuration:
  - LED0: GPIO pin 2 (onboard)
  - LED1: GPIO pin 25
  - LED2: GPIO pin 26

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
import time


def irq_timer0(t):
    """Interrupt handler of Timer0"""
    led0.value(not led0.value())


def irq_timer1(t):
    """Interrupt handler of Timer1"""
    led1.value(not led1.value())


def irq_timer2(t):
    """Interrupt handler of Timer2"""
    led2.value(not led2.value())


# Create an object for on-board and other LEDs
led0 = Pin(2, mode=Pin.OUT)
led1 = Pin(25, mode=Pin.OUT)
led2 = Pin(26, mode=Pin.OUT)

# Create and init objects for 64-bit timers
timer0 = Timer(0)  # Between 0-3 for ESP32
timer1 = Timer(1)
timer2 = Timer(2)
timer0.init(mode=Timer.PERIODIC, period=100, callback=irq_timer0)
timer1.init(mode=Timer.PERIODIC, period=200, callback=irq_timer1)
timer2.init(mode=Timer.PERIODIC, period=500, callback=irq_timer2)

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        # print("Running...")
        # time.sleep(0.1)
        pass
except KeyboardInterrupt:
    timer0.deinit()
    timer1.deinit()
    timer2.deinit()
    print("Ctrl+C Pressed. Exiting...")
