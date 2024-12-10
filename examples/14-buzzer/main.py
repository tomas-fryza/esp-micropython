# Source:
# https://micropython-on-wemos-d1-mini.readthedocs.io/en/latest/basics.html#beepers
#
# FireBeelte v2 pinout:
# https://image.dfrobot.com/image/data/DFR0654/pinout.png

from machine import Pin
from machine import PWM
import time

tones = {
    'c': 262,  # https://muted.io/note-frequencies/
    'd': 294,
    'e': 330,
    'f': 349,
    'g': 392,
    'a': 440,
    'b': 494,
    'C': 523,
    ' ': 1,
    }
tempo = 3

# Frequency can be from 1 Hz to 40 MHz
# 10-bit duty range 0--1023 (default 512, 50%)
beeper = PWM(Pin(17, Pin.OUT), freq=440, duty=512)

melody = 'cde fgabC'
rhythm = [8, 8, 8, 8, 8, 8, 8, 8, 8]

# zip() is used to combine two iterables into "tone" and "length"
for tone, length in zip(melody, rhythm):
    print(f"Tone: {tone} \tDuration: {tempo/length}")
    beeper.freq(tones[tone])
    time.sleep(tempo/length)

beeper.deinit()
