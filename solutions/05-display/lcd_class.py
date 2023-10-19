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


class LCD

    def __init__(self, RS, E, D7, D6, D5, D4):
        self.RS = Pin(RS, Pin.OUT)
        self.E = Pin(E, Pin.OUT)
        self.D = [Pin(D7, Pin.OUT), Pin(D6, Pin.OUT), Pin(D5, Pin.OUT), Pin(D4, Pin.OUT)]

        self._init()


    def _init(self):
        """Initialization sequence of HD44780"""
        # All commands will be sent
        self.RS.off()
        time.sleep_ms(20)
        write_nibble(0x30)
        time.sleep_ms(5)
        write_nibble(0x30)
        time.sleep_ms(1)
        write_nibble(0x30)
        time.sleep_ms(1)
        write_nibble(0x20)
        time.sleep_ms(1)
        command(0x28)  # 4-bit, 2 lines, 5x7 pixels
        command(0x06)  # Increment, no shift
        command(0x01)  # Clear display
        # command(0x0f)  # Display on, cursor on and blinking
        # command(0x0e)  # Display on, cursor on but not blinking
        command(0x0c)  # Display on, cursor off


    def _set_data_bits(self, val):
        """Set four data pins according to the parameter val"""
        for i in range(4):
            # For each pin, set the value according to the corresponding bit
            self.D[i].value(val & (1 << (i + 4)))


    def _write_nibble(self, val):
        """Write upper nibbble of the value byte"""
        self._set_data_bits(val)
        self.E.on()
        time.sleep_us(1)
        self.E.off()


    def _write_byte(self, val):
        """Write a byte of value to the LCD controller"""
        self._write_nibble(val)       # Write upper nibble
        self._write_nibble(val << 4)  # Write lower nibble


    def command(self, cmd):
        """Write a command to the LCD controller"""
        # RS pin = 0, write to command register
        self.RS.off()
        # Write the command
        self._write_byte(cmd)
        time.sleep_ms(2)


    def data(self, val):
        """Write data to the LCD controller"""
        # RS pin = 1, write to data register
        self.RS.on()
        # Write the data
        self._write_byte(val)


    def put_string(self, s):
        """Display a character string on the LCD"""
        for c in s:
            self.data(ord(c))


    def cursor(self, line, column):
        """Move cursor to a specified location of the display"""
        if line == 1:
            cmd = 0x80
        elif line == 2:
            cmd = 0xc0
        else:
            return

        if column < 1 or column > 20:
            return

        cmd += column - 1
        self.command(cmd)
