"""
MicroPython HD44780 Character LCD Controller

This class provides a simple interface to control character LCDs
based on the HD44780 driver. It allows you to display text and
control the cursor position on the LCD screen.

Compatible with ESP32 boards and other MicroPython-supported hardware.

Author(s): Shujen Chen et al. Raspberry Pi Pico Interfacing and
           Programming with MicroPython
           Tomas Fryza
Date: 2023-10-17
"""

import time              # For time delays
from machine import Pin  # For GPIO control


class LcdHd44780:
    def __init__(self, pin_rs, pin_e=3, pins_data=(25, 26, 27, 9)):
        # Create a machine.Pin object within the constructor
        self.LCD_RS = Pin(pin_rs, Pin.OUT)


    def toggle(self):
        self.LCD_RS.value(not self.LCD_RS.value())


if __name__ == "__main__":
    # lcd = Lcd(pin_rs=1, pin_e=3, pins_data=(25, 26, 27, 9))
    lcd = LcdHd44780(pin_rs=2)  # Example GPIO pin number (change as needed)
    lcd.toggle()  # Toggles the pin state
