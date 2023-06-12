# main.py
#
# Blink the on-board LED

from machine import Pin
from time import sleep

# Check the LED pin on your board, usually it is `2`
PIN_LED = 2


def main():
    led = Pin(PIN_LED, Pin.OUT)

    while True:
        led.value(1)
        sleep(0.75)
        led(False)
        sleep(0.25)


if __name__ == "__main__":
    main()
