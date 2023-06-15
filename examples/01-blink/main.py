"""Blink the on-board LED.

A simple example of how to control one output pin of 
a microcontroller. An LED is connected to the GPIO pin,
which is repeatedly switched on and off.
"""

from machine import Pin
from time import sleep_ms

# Check the LED pin on your board, usually it is GPIO2
PIN_LED = 2


def main():
    print("Configure output pin...", end="")
    led = Pin(PIN_LED, Pin.OUT)
    print("Done")
    print(f"Start blinking pin {PIN_LED}")

    # Forever loop
    while True:
        led.on()
        sleep_ms(750)
        led.off()
        sleep_ms(250)

"""Top-level code is executed when the program is run directly
by the Python interpreter. Note that the code inside the if
statement is not executed when the file's code is imported
as a module.
"""
if __name__ == "__main__":
    main()
