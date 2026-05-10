"""
Read the rotary encoder value

Requires: rotary_irq and rotary modules

Authors:
- Tomas Fryza
- https://easyeda.com/editor#id=4e272acacecf42169229b9288f3defe5|5251c125583f4b4985e5f40a20381136

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
PIN_ROT_A = 35  # Warning: No internal pull-up
                # https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
PIN_ROT_B = 32


def btn_rot_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        print(f"Rot. encoder pressed: {pin}")


# Rotary encoder
rot = RotaryIRQ(pin_num_clk=PIN_ROT_A,
                pin_num_dt=PIN_ROT_B,
                min_val=0,
                max_val=15,
                range_mode=RotaryIRQ.RANGE_BOUNDED,  # Stops at min/max values
                pull_up=True)
prev_val = rot.value()

btn_rot = Pin(PIN_ROT_BTN, Pin.IN, pull=Pin.PULL_UP)
# btn_rot_a = Pin(PIN_ROT_A, Pin.IN, pull=Pin.PULL_UP)
# btn_rot_b = Pin(PIN_ROT_B, Pin.IN, pull=Pin.PULL_UP)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        current_val = rot.value()
        print(current_val)

        if current_val != prev_val:
            print(f"Volume: {current_val}")

            prev_val = current_val

        time.sleep_ms(50)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    btn_rot.irq(handler=None)
