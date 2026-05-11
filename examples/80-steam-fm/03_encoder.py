"""
Read the rotary encoder value

Requires: rotary_irq and rotary modules

Authors:
- Tomas Fryza
- https://easyeda.com/editor#id=4e272acacecf42169229b9288f3defe5|5251c125583f4b4985e5f40a20381136

Creation date: 2025-03-05
Last modified: 2026-05-11

Inspired by:
  * https://techtotinker.com/2021/04/13/027-micropython-technotes-rotary-encoder/
"""

# MicroPython builtin modules
from machine import Pin
import time

# External modules
from rotary_irq import RotaryIRQ  # Rotary encoder

# --- Set your pins --------------------------
# Rotary encoder
ROT_BTN = 33
ROT_A = 35  # Warning: No internal pull-up on pin 35
            # https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
ROT_B = 32
# --------------------------------------------


# Interrupt callback
def btn_rot_isr(pin):
    time.sleep_ms(50)
    if pin.value() == 0:
        print(f"Rot. encoder pressed: {pin}")


# Init rotary encoder
rot = RotaryIRQ(pin_num_clk=ROT_A,
                pin_num_dt=ROT_B,
                min_val=0,
                max_val=15,
                range_mode=RotaryIRQ.RANGE_BOUNDED,  # Stops at min/max values
                pull_up=True)
prev_val = rot.value()

btn_rot = Pin(ROT_BTN, Pin.IN, pull=Pin.PULL_UP)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

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
