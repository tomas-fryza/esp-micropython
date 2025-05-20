"""
Read the rotary encoder value

Requires: rotary_irq and rotary modules

Authors:
- Tomas Fryza

Creation date: 2025-03-05
Last modified: 2025-05-20

Inspired by:
  * https://techtotinker.com/2021/04/13/027-micropython-technotes-rotary-encoder/
"""

# MicroPython builtin modules
from machine import Pin
from machine import PWM
import time

# External modules
from rotary_irq import RotaryIRQ  # Rotary encoder

# Set your pins
PIN_ROT_BTN = 33  # Rotary encoder
PIN_ROT_A = 35
PIN_ROT_B = 32

PIN_BUZ = 13  # Buzzer


def btn_rot_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        print(f"Rot. encoder pressed: {pin}")
        beep()


def beep(freq=1500, duration_ms=60, duty_cycle=40):
    buzzer.freq(freq)
    buzzer.duty(duty_cycle)
    time.sleep_ms(duration_ms)
    buzzer.duty(0)


# Rotary encoder
rot = RotaryIRQ(pin_num_clk=PIN_ROT_A,
                pin_num_dt=PIN_ROT_B,
                min_val=0,
                max_val=15,
                range_mode=RotaryIRQ.RANGE_BOUNDED)  # Stops at min/max values
prev_val = rot.value()

btn_rot = Pin(PIN_ROT_BTN, Pin.IN)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

# Start buzzer with duty=0 (silent)
buzzer = PWM(Pin(PIN_BUZ, Pin.OUT), duty=0)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        current_val = rot.value()

        if current_val != prev_val:
            print(f"Volume: {current_val}")

            prev_val = current_val

        time.sleep_ms(50)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    btn_rot.irq(handler=None)
    buzzer.deinit()
