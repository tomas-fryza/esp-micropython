# ------------------------------------------------------------
# ESP32 FM Radio Example (MicroPython)
#
# Features:
# - RDA5807 FM radio
# - SH1106 OLED display
# - Rotary encoder volume control
# - Button interrupts using event flags
# - LEDs
#
# Authors:
# - Tomas Fryza
# - Ondrej Kolar
#
# Creation date: 2025-01-23
# Last modified: 2026-05-12
#
# Inspired by:
#   * https://101-things.readthedocs.io/en/latest/fm_radio.html
#   * https://github.com/franckinux/python-rd5807m/tree/master
#   * https://github.com/wagiminator/ATtiny85-TinyFMRadio/blob/master/software/TinyFMRadio.ino
#   * https://github.com/pu2clr/RDA5807/tree/master/examples
# ------------------------------------------------------------

# Micropython builtin modules
from machine import Pin, I2C
import time

# External modules
from sh1106 import SH1106_I2C
from rotary_irq import RotaryIRQ
import rda5807

# ------------------------------------------------------------
# Pin configuration
# ------------------------------------------------------------
BTN_LEFT = 26
BTN_RIGHT = 14

LED_0 = 19
LED_1 = 18
LED_2 = 5

ROT_BTN = 33
ROT_A = 35  # GPIO35 has NO internal pull-up
ROT_B = 32

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
DISPLAY_REFRESH_MS = 500
DEBOUNCE_MS = 200

START_FREQUENCY = 88.3

# ------------------------------------------------------------
# Event flags
# ------------------------------------------------------------
seek_up_requested = False
seek_down_requested = False
mute_requested = False

# ------------------------------------------------------------
# Debounce timers
# ------------------------------------------------------------
last_left_press = 0
last_right_press = 0
last_rot_press = 0

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def init_display(i2c):
    """Initialize OLED display."""
    display = SH1106_I2C(i2c)
    display.fill(0)
    display.show()
    return display


def update_display(display, radio, volume, mute):
    """Refresh OLED content."""

    display.fill(0)

    # Station name
    radio_name = "".join(radio.station_name)
    display.text(radio_name, 0, 0)

    # Frequency
    freq = radio.get_frequency_MHz()
    display.text(f"{freq:.1f} MHz", 0, 12)

    # Volume
    display.text(f"Volume: {volume}", 0, 24)

    # Signal strength
    rssi = radio.get_signal_strength()
    display.text(f"RSSI: {rssi} dBm", 0, 36)

    # Mute status
    if mute:
        display.text("MUTED", 0, 48)

    display.show()


# ------------------------------------------------------------
# Interrupt handlers
#
# IMPORTANT:
# Interrupt handlers should stay SHORT.
# Do not:
# - print()
# - sleep()
# - use I2C
# - allocate memory
#
# We only set event flags here.
# ------------------------------------------------------------
def btn_left_isr(pin):
    global seek_down_requested
    global last_left_press

    now = time.ticks_ms()

    if time.ticks_diff(now, last_left_press) > DEBOUNCE_MS:
        seek_down_requested = True
        last_left_press = now


def btn_right_isr(pin):
    global seek_up_requested
    global last_right_press

    now = time.ticks_ms()

    if time.ticks_diff(now, last_right_press) > DEBOUNCE_MS:
        seek_up_requested = True
        last_right_press = now


def btn_rot_isr(pin):
    global mute_requested
    global last_rot_press

    now = time.ticks_ms()

    if time.ticks_diff(now, last_rot_press) > DEBOUNCE_MS:
        mute_requested = True
        last_rot_press = now

# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------
if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
    display = init_display(i2c)
    radio = rda5807.Radio(i2c)
    # IMPORTANT:
    # Give radio chip time to initialize
    time.sleep_ms(100)

    # Buttons
    btn_left = Pin(BTN_LEFT, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(BTN_RIGHT, Pin.IN, Pin.PULL_UP)
    btn_rot = Pin(ROT_BTN, Pin.IN, Pin.PULL_UP)

    # Attach buttons' interrupts
    btn_left.irq(
        trigger=Pin.IRQ_FALLING,
        handler=btn_left_isr
    )
    btn_right.irq(
        trigger=Pin.IRQ_FALLING,
        handler=btn_right_isr
    )
    btn_rot.irq(
        trigger=Pin.IRQ_FALLING,
        handler=btn_rot_isr
    )

    # LEDs
    led_up = Pin(LED_0, Pin.OUT)
    led_down = Pin(LED_1, Pin.OUT)
    led_mute = Pin(LED_2, Pin.OUT)

    # Rotary encoder
    rot = RotaryIRQ(
        pin_num_clk=ROT_A,
        pin_num_dt=ROT_B,
        min_val=0,
        max_val=15,
        range_mode=RotaryIRQ.RANGE_BOUNDED,  # Stops at min/max values
        pull_up=True)

    volume = 0
    prev_volume = volume

    # Set FM module
    radio.set_frequency_MHz(START_FREQUENCY)
    radio.set_volume(volume)

    mute = False
    radio.mute(mute)

    last_display_update = 0

    print("FM radio running. Press Ctrl+C to stop.")

    try:
        while True:
            # ------------------------------------------------
            # Handle SEEK UP request
            # ------------------------------------------------
            if seek_up_requested:
                seek_up_requested = False
                print("Seek up")
                led_up.on()
                radio.seek_up()
                led_up.off()

            # ------------------------------------------------
            # Handle SEEK DOWN request
            # ------------------------------------------------
            if seek_down_requested:
                seek_down_requested = False
                print("Seek down")
                led_down.on()
                radio.seek_down()
                led_down.off()

            # ------------------------------------------------
            # Handle MUTE request
            # ------------------------------------------------
            if mute_requested:
                mute_requested = False
                mute = not mute
                radio.mute(mute)
                led_mute.value(mute)
                print(f"Mute: {mute}")

            # ------------------------------------------------
            # Rotary encoder volume
            # ------------------------------------------------
            volume = rot.value()
            if volume != prev_volume:
                prev_volume = volume
                radio.set_volume(volume)
                print(f"Volume: {volume}")

            # ------------------------------------------------
            # Update RDS information
            # ------------------------------------------------
            radio.update_rds()

            # ------------------------------------------------
            # Update display periodically
            # ------------------------------------------------
            now = time.ticks_ms()
            if time.ticks_diff(now, last_display_update) > DISPLAY_REFRESH_MS:
                update_display(
                    display,
                    radio,
                    volume,
                    mute
                )
                last_display_update = now

            # Small delay reduces CPU usage
            time.sleep_ms(20)

    # --------------------------------------------------------
    # Exit program
    # --------------------------------------------------------
    except KeyboardInterrupt:
        print("\nStopping program...")

        # Disable interrupts
        btn_left.irq(handler=None)
        btn_right.irq(handler=None)
        btn_rot.irq(handler=None)

        # Turn off LEDs
        led_up.off()
        led_down.off()
        led_mute.off()

        # Shutdown peripherals
        display.poweroff()
        radio.mute(True)

        print("Cleanup complete.")
