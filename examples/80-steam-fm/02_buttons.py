"""
Buttons

Authors:
- Tomas Fryza
- https://easyeda.com/editor#id=4e272acacecf42169229b9288f3defe5|5251c125583f4b4985e5f40a20381136

Creation date: 2025-05-18
Last modified: 2026-05-10
"""

from machine import Pin
from machine import PWM
import time


# Set your pins
PIN_LED_0 = 19
PIN_LED_1 = 18
PIN_LED_2 = 5
PIN_LED_3 = 2

PIN_BTN_0 = 26  # Left
PIN_BTN_1 = 14  # Right
PIN_BTN_2 = 25  # Up
PIN_BTN_3 = 27  # Down
PIN_ROT_BTN = 33  # Rotary encoder


# Interrupt callbacks
def btn_0_isr(pin):
    # Debounce delay
    time.sleep_ms(50)
    if pin.value() == 0:  # Button pressed (active-low)
        led_0.value(not led_0.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_0.value()}")


def btn_1_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        led_1.value(not led_1.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_1.value()}")


def btn_2_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        led_2.value(not led_2.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_2.value()}")


def btn_3_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        led_3.value(not led_3.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_3.value()}")


def btn_rot_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        print(f"Rot. encoder pressed: {pin}")


# LEDs
led_0 = Pin(PIN_LED_0, Pin.OUT)
led_1 = Pin(PIN_LED_1, Pin.OUT)
led_2 = Pin(PIN_LED_2, Pin.OUT)
led_3 = Pin(PIN_LED_3, Pin.OUT)

# Buttons
btn_0 = Pin(PIN_BTN_0, Pin.IN, pull=Pin.PULL_UP)
btn_1 = Pin(PIN_BTN_1, Pin.IN, pull=Pin.PULL_UP)
btn_2 = Pin(PIN_BTN_2, Pin.IN, pull=Pin.PULL_UP)
btn_3 = Pin(PIN_BTN_3, Pin.IN, pull=Pin.PULL_UP)
btn_rot = Pin(PIN_ROT_BTN, Pin.IN, pull=Pin.PULL_UP)

# Attach buttons' interrupts
btn_0.irq(trigger=Pin.IRQ_FALLING, handler=btn_0_isr)
btn_1.irq(trigger=Pin.IRQ_FALLING, handler=btn_1_isr)
btn_2.irq(trigger=Pin.IRQ_FALLING, handler=btn_2_isr)
btn_3.irq(trigger=Pin.IRQ_FALLING, handler=btn_3_isr)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

# Start buzzer with duty=0 (silent)
# buzzer = PWM(Pin(PIN_BUZ, Pin.OUT), duty=0)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_0.off()
    led_1.off()
    led_2.off()
    led_3.off()
    btn_0.irq(handler=None)  # Disables IRQ triggers
    btn_1.irq(handler=None)
    btn_2.irq(handler=None)
    btn_3.irq(handler=None)
    btn_rot.irq(handler=None)
    # buzzer.deinit()
