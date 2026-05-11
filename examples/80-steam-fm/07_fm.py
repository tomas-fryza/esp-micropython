"""
FM radio

Key functionalities of this MicroPython script include controlling
the FM radio's volume and frequency, and updating the OLED display
with RDS data.

Authors:
- Tomas Fryza
- Ondrej Kolar

Creation date: 2025-01-23
Last modified: 2026-05-10

Inspired by:
  * https://101-things.readthedocs.io/en/latest/fm_radio.html
  * https://github.com/franckinux/python-rd5807m/tree/master
  * https://github.com/wagiminator/ATtiny85-TinyFMRadio/blob/master/software/TinyFMRadio.ino
  * https://github.com/pu2clr/RDA5807/tree/master/examples
"""

# Micropython builtin modules
from machine import Pin, I2C
import time

# External modules
from sh1106 import SH1106_I2C
from rotary_irq import RotaryIRQ  # Rotary encoder
import rda5807                    # FM radio module


# --- Set your pins --------------------------
BTN_LEFT = 26
BTN_RIGHT = 14

LED_0 = 19
LED_1 = 18
LED_2 = 5

# Rotary encoder
ROT_BTN = 33
ROT_A = 35  # Warning: No internal pull-up on pin 35
ROT_B = 32
# --------------------------------------------


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    display = SH1106_I2C(i2c)
    display.fill(0)
    return display


# Interrupt callbacks
def btn_left_isr(pin):
    led_down.on()
    time.sleep_ms(20)  # Debounce delay
    if pin.value() == 0:  # Button pressed (active-low)
        print(f"Btn {pin} pressed: Seek down")
        radio.seek_down()
    led_down.off()


def btn_right_isr(pin):
    led_up.on()
    time.sleep_ms(20)
    if pin.value() == 0:
        print(f"Btn {pin} pressed: Seek up")
        radio.seek_up()
    led_up.off()


def btn_rot_isr(pin):
    global mute

    time.sleep_ms(20)
    if pin.value() == 0:
        mute = not mute
        radio.mute(mute)
        print(f"Mute radio: {mute}")
        led_mute.value(not led_mute.value())


if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
    display = init_display(i2c)
    radio = rda5807.Radio(i2c)
    time.sleep_ms(100)  # Let the radio initialize !!! Otherwise the module does not work !!!

    # Buttons
    btn_left = Pin(BTN_LEFT, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(BTN_RIGHT, Pin.IN, Pin.PULL_UP)
    btn_rot = Pin(ROT_BTN, Pin.IN, Pin.PULL_UP)

    # Attach buttons' interrupts
    btn_left.irq(trigger=Pin.IRQ_FALLING, handler=btn_left_isr)
    btn_right.irq(trigger=Pin.IRQ_FALLING, handler=btn_right_isr)
    btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

    # LEDs
    led_up = Pin(LED_0, Pin.OUT)
    led_down = Pin(LED_1, Pin.OUT)
    led_mute = Pin(LED_2, Pin.OUT)

    # Rotary encoder
    rot = RotaryIRQ(pin_num_clk=ROT_A,
                    pin_num_dt=ROT_B,
                    min_val=0,
                    max_val=15,
                    range_mode=RotaryIRQ.RANGE_BOUNDED,  # Stops at min/max values
                    pull_up=True)
    prev_val = rot.value()

    # Set FM module
    radio.set_frequency_MHz(88.3)  # 88.3 - Kiss
    radio.set_volume(prev_val)     # 0--15
    mute = False
    radio.mute(mute)
    radio_text = ""

    print("Press `Ctrl+C` to stop")

    try:
        while True:
            # Clear display
            display.fill(0)

            # Rotary
            current_val = rot.value()
            if current_val != prev_val:
                print(f"Volume: {current_val}")
                radio.set_volume(current_val)
                prev_val = current_val

            # FM Radio
            radio.update_rds()
            radio_name = "".join(map(str, radio.station_name))
            display.text(str(radio_name), 0, 0, 1)

            radio_text_new = "".join(map(str, radio.radio_text))
            if radio_text != radio_text_new:
                radio_text = radio_text_new
                print(f"RDS text: {radio_text}")

            display.text(f"{str(radio.get_frequency_MHz())} MHz", 30, 8, 1)
            display.text(f"volume: {str(prev_val)}", 0, 24, 1)

            rssi = radio.get_signal_strength()
            display.text(f"signal: {str(rssi)} dBm", 0, 32, 1)

            display.show()
            time.sleep(1)

    except KeyboardInterrupt:
        # This part runs when Ctrl+C is pressed
        print("\nProgram stopped. Exiting...")

        # Optional cleanup code
        btn_left.irq(handler=None)  # Disables IRQ triggers
        btn_right.irq(handler=None)
        btn_rot.irq(handler=None)

        led_up.off()
        led_down.off()
        led_mute.off()

        display.poweroff()
        radio.mute(True)
