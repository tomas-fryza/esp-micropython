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

# import time              # For time delays
from machine import Pin  # For GPIO control


class MyDevice:
    def __init__(self, pin0, pin1, pin2):
        # Create a machine.Pin object within the constructor
        self.pin0 = Pin(pin0, Pin.OUT)
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin2 = Pin(pin2, Pin.OUT)
        # self.LCD_D = [Pin(pin, Pin.OUT) for pin in pins_data]
        print(self)


    def toggle(self):
        self.pin0.value(not self.pin0.value())


# rs_pin = 2  # Spravne: 1
# e_pin = 3
# data_pins = (25, 26, 27, 9)
# lcd = LcdHd44780(2, 3, (25, 26, 27, 9))
# lcd.toggle()  # Toggles the pin state



my_device = MyDevice(2,3,25)  # Example GPIO pin number (change as needed)
my_device.toggle()  # Toggles the pin state

