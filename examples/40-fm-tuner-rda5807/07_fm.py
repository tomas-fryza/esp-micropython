"""
FM radio

Key functionalities of this MicroPython script include controlling
the FM radio's volume and frequency, and updating the OLED display
with RDS data.

Authors:
- Tomas Fryza
- Ondrej Kolar

Creation date: 2025-01-23
Last modified: 2025-05-19

Inspired by:
  * https://101-things.readthedocs.io/en/latest/fm_radio.html
  * https://github.com/franckinux/python-rd5807m/tree/master
  * https://github.com/wagiminator/ATtiny85-TinyFMRadio/blob/master/software/TinyFMRadio.ino
  * https://github.com/pu2clr/RDA5807/tree/master/examples
"""

# Micropython builtin modules
from machine import Pin
from machine import SoftI2C
from machine import PWM
import time

# External modules
import ssd1306                    # OLED display
from rotary_irq import RotaryIRQ  # Rotary encoder
import rda5807                    # FM radio module


# Set your pins
PIN_BTN_0 = 4  # Left
PIN_BTN_1 = 0  # Right

PIN_ROT_BTN = 33  # Rotary encoder
PIN_ROT_A = 35
PIN_ROT_B = 32

PIN_BUZ = 13  # Buzzer

PIN_SHDN = 26  # PAM8008 class-D amplifier
PIN_MUTE = 27
PIN_VOLUME = 25


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.contrast(100)
    display.fill(0)
    return display


# Interrupt callbacks
def btn_0_isr(pin):  # Left button
    # Debounce delay
    time.sleep_ms(20)
    if pin.value() == 0:  # Button pressed (active-low)
        radio.seek_up()
        print(f"Btn pressed: {pin}")


def btn_1_isr(pin):  # Right button
    time.sleep_ms(20)
    if pin.value() == 0:
        radio.seek_down()
        print(f"Btn pressed: {pin}")


def btn_rot_isr(pin):
    global mute

    time.sleep_ms(20)
    if pin.value() == 0:
        mute = not mute
        radio.mute(mute)
        print(f"Mute radio: {mute}")
        beep()


def beep(freq=1500, duration_ms=60, duty_cycle=40):
    buzzer.freq(freq)
    buzzer.duty(duty_cycle)
    time.sleep_ms(duration_ms)
    buzzer.duty(0)


i2c = SoftI2C(sda=Pin(21), scl=Pin(22))

# I2C devices
display = init_display(i2c)
radio = rda5807.Radio(i2c)
time.sleep_ms(100)  # Let the radio initialize !!! Otherwise the module does not work !!!

# Buttons
btn_0 = Pin(PIN_BTN_0, Pin.IN)
btn_1 = Pin(PIN_BTN_1, Pin.IN)
btn_rot = Pin(PIN_ROT_BTN, Pin.IN)

# Attach buttons' interrupts
btn_0.irq(trigger=Pin.IRQ_FALLING, handler=btn_0_isr)
btn_1.irq(trigger=Pin.IRQ_FALLING, handler=btn_1_isr)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

# Start buzzer with duty=0 (silent)
buzzer = PWM(Pin(PIN_BUZ, Pin.OUT), duty=0)

# Rotary encoder
rot = RotaryIRQ(pin_num_clk=PIN_ROT_A,
                pin_num_dt=PIN_ROT_B,
                min_val=0,
                max_val=15,
                range_mode=RotaryIRQ.RANGE_BOUNDED)  # Stops at min/max values
prev_val = rot.value()

# Set FM module
radio.set_frequency_MHz(103.4)  # 103.4 - Blanik
radio.set_volume(prev_val)      # 0--15
mute = False
radio.mute(mute)
radio_text = ""

# PAM8008 class-D amplifier
shdn = Pin(PIN_SHDN, Pin.OUT)
shdn.value(1)  # Disable shutdown
mute_pin = Pin(PIN_MUTE, Pin.OUT)
mute_pin.value(0)  # Disable mute
volume = Pin(PIN_VOLUME, Pin.OUT)
volume.value(0)  # Set maximal volume

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Clear display
        display.fill(0)

        current_val = rot.value()

        if current_val != prev_val:
            radio.set_volume(current_val)

            print(f"Volume: {current_val}")

            prev_val = current_val

        # FM Radio
        radio.update_rds()
        radio_name = "".join(map(str, radio.station_name))
        display.text(str(radio_name), 0, 0, 1)

        radio_text_new = "".join(map(str, radio.radio_text))
        if radio_text != radio_text_new:
            radio_text = radio_text_new
            print(f"RDS text: {radio_text}")

        display.text(f"{str(radio.get_frequency_MHz())} MHz", 0, 8, 1)
        display.text(f"volume: {str(prev_val)}", 0, 24, 1)

        rssi = radio.get_signal_strength()
        display.text(f"strength: {str(rssi)} dBm", 0, 32, 1)

        display.show()
        time.sleep_ms(20)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    btn_0.irq(handler=None)  # Disables IRQ triggers
    btn_1.irq(handler=None)
    btn_rot.irq(handler=None)
    buzzer.deinit()
    display.poweroff()
    shdn.value(0)
