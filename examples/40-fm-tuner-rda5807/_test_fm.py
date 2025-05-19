"""
FM radio & sensors

Key functionalities of this MicroPython script include controlling
the FM radio's volume and frequency, measuring temperature and
pressure data, and updating the OLED display with real-time
sensor readings.

Authors:
- Tomas Fryza
- Ondrej Kolar

Creation date: 2025-01-23
Last modified: 2025-05-19

Inspired by:
FM RDA5807M
  * https://101-things.readthedocs.io/en/latest/fm_radio.html
  * https://github.com/franckinux/python-rd5807m/tree/master
  * https://github.com/wagiminator/ATtiny85-TinyFMRadio/blob/master/software/TinyFMRadio.ino
  * https://github.com/pu2clr/RDA5807/tree/master/examples

Rotary Encoder
  * https://techtotinker.com/2021/04/13/027-micropython-technotes-rotary-encoder/
"""

# Micropython builtin modules
import time
from machine import Pin, SoftI2C, RTC, PWM

# External modules
import ssd1306                    # OLED display
from bmp180 import BMP180         # Pressure meter
import rda5807                    # FM radio module
from rotary_irq import RotaryIRQ  # Rotary encoder

LED_PIN = 2
BTN_UP_PIN = 19
BTN_DOWN_PIN = 18
ROT_PIN = 33
ROT_CLK_PIN = 32
ROT_DT_PIN = 35
# BUZZ_PIN = 13
PIR_PIN = 15


def button_mute(pin):
    global led, mute

    led.on()
    time.sleep_ms(20)
    mute = not mute
    radio.mute(mute)
    print(f"Mute: {mute}")


# Init I2C using pins 22 & 21 (default I2C pins)
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))  #, freq=400_000)
print(f"I2C configuration : {str(i2c)}")

# I2C devices
display = ssd1306.SSD1306_I2C(128, 32, i2c)
bmp180 = BMP180(i2c)
radio = rda5807.Radio(i2c)
time.sleep_ms(100)  # Let the radio initialize !!! Otherwise the module does not work !!!

# Led & buttons
led = Pin(LED_PIN, Pin.OUT)
btn_up = Pin(BTN_UP_PIN, Pin.IN, Pin.PULL_UP)
btn_down = Pin(BTN_DOWN_PIN, Pin.IN, Pin.PULL_UP)
btn_rot = Pin(ROT_PIN, Pin.IN, Pin.PULL_UP)

# Attach interrupt to the button pin (trigger on falling edge)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=button_mute)

# Other devices
# buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT), duty=0)  # duty=0 prevents default waveform from starting immediately
pir = Pin(PIR_PIN, Pin.IN)
rot = RotaryIRQ(pin_num_clk=ROT_CLK_PIN,
                pin_num_dt=ROT_DT_PIN,
                min_val=0,
                max_val=15,
                pull_up=False,
                half_step=True,
                reverse=False,
                range_mode=RotaryIRQ.RANGE_BOUNDED)

# Set FM module
vol = rot.value()
mute = False
radio_text = ""
radio.set_volume(vol)           # 0--15
radio.set_frequency_MHz(103.4)  # 103.4 - Blanik
radio.mute(mute)

print("\nStart using FM module and sensors. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        # Clear display
        display.fill(0)

        # Volume 0--15
        vol_new = rot.value()
        if vol != vol_new:
            vol = vol_new
            radio.set_volume(vol)
            print(f"Volume: {vol}")
        display.text('vol: '+str(vol), 0, 16, 1)

        # Buttons: seek frequency up, down, and mute
        if (btn_up.value() == 0):
            led.on()
            radio.seek_up()
        elif (btn_down.value() == 0):
            led.on()
            radio.seek_down()
        else:
            led.off()

        # BMPT180: air temperature and pressure
        pressure = f"{bmp180.pressure/100:.1f} hPa"
        display.text(pressure, 60, 16, 1)
        temperature = f"{bmp180.temperature:.1f} C"
        display.text(temperature, 60, 24, 1)

        # Passive infrared, motion detection
        display.text('PIR: '+str(pir.value()), 0, 24, 1)

        # FM Radio
        radio.update_rds()
        radio_name = "".join(map(str, radio.station_name))
        display.text(str(radio_name), 0, 0, 1)

        radio_text_new = "".join(map(str, radio.radio_text))
        if radio_text != radio_text_new:
            radio_text = radio_text_new
            print(f"RDS text: {radio_text}")

        display.text(str(radio.get_frequency_MHz())+' MHz', 0, 8, 1)

        rssi = radio.get_signal_strength()
        display.text(str(rssi)+' dBm', 85, 8, 1)

        display.show()
        time.sleep_ms(20)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led.off()
    # buzzer.deinit()
