"""
This module provides a simple interface for controlling character LCDs
based on the HD44780 driver. It supports displaying text, controlling the
cursor position, and creating custom characters on the LCD screen.

Example
-------
.. code-block:: python

    from machine import Pin
    import time
    from lcd_hd44780 import LcdHd44780

    # Initialize the LCD with control pins (RS, E) and data pins (D4, D5, D6, D7)
    lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

    # Move cursor to line 1, column 3 and display text
    lcd.move_to(1, 3)
    lcd.write("Hello, World!")

    lcd.move_to(2, 5)
    lcd.write("MicroPython")

Authors
-------
- Shujen Chen et al. Raspberry Pi Pico Interfacing and Programming with MicroPython
- Tomas Fryza

Modification history
--------------------
- **2024-11-11** : Added Sphinx-style comments for documentation.
- **2024-10-26** : Added `demo` method to demonstrate usage of the display.
- **2023-10-17** : File created, initial release.
"""

from machine import Pin
import time


class LcdHd44780:
    def __init__(self, rs, e, d):
        """
        Initialize the LCD with control (RS, E) and data (D4-D7) pins.

        :param rs: Pin number for the RS (Register Select) pin.
        :param e: Pin number for the E (Enable) pin.
        :param d: List of pin numbers for the data pins (D4-D7).
        """
        # Create machine.Pin objects within the constructor
        self.RS = Pin(rs, Pin.OUT)
        self.E = Pin(e, Pin.OUT)
        self.D = [Pin(pin_number, Pin.OUT) for pin_number in d]
        # Send initialization sequence
        self._init()

    def _init(self):
        """
        Initialize the HD44780 LCD controller with a predefined sequence of
        commands. This method is automatically called in the constructor.
        """
        self.RS.off()
        time.sleep_ms(20)
        self._write_nibble(0x30)
        time.sleep_ms(5)
        self._write_nibble(0x30)
        time.sleep_ms(1)
        self._write_nibble(0x30)
        time.sleep_ms(1)
        self._write_nibble(0x20)
        time.sleep_ms(1)
        self.command(0x28)  # 4-bit, 2 lines, 5x7 pixels
        self.command(0x06)  # Increment, no shift
        self.command(0x01)  # Clear display
        
        # Select one command:
        # self.command(0x0f)  # Display on, cursor on and blinking
        # self.command(0x0e)  # Display on, cursor on but not blinking
        self.command(0x0c)  # Display on, cursor off

    def _set_data_bits(self, val):
        """
        Set the data pins (D4-D7) based on the provided value.

        :param val: A 8-bit value where the upper 4 bits are sent to the data pins.
        """
        for i in range(4):
            # For each pin, set the value according to the corresponding bit
            self.D[i].value(val & (1 << (i + 4)))

    def _write_nibble(self, val):
        """
        Write the upper nibble (4 bits) of the byte to the LCD.

        :param val: The upper 4 bits of the byte to write to the LCD.
        """
        self._set_data_bits(val)
        self.E.on()
        time.sleep_us(1)
        self.E.off()

    def _write_byte(self, val):
        """
        Write a byte to the LCD controller by sending both the upper and
        lower nibbles.

        :param val: The byte to write to the LCD (8 bits).
        """
        self._write_nibble(val)  # Write upper nibble
        self._write_nibble(val << 4)  # Write lower nibble

    def command(self, cmd):
        """
        Send a command byte to the LCD controller. This method writes to
        the command register of the LCD (RS = 0).

        :param cmd: The command byte to send to the LCD.
        """
        # RS pin = 0, write to command register
        self.RS.off()
        # Write the command
        self._write_byte(cmd)
        time.sleep_ms(2)

    def data(self, val):
        """
        Send a data byte to the LCD controller. This method writes to
        the data register of the LCD (RS = 1).

        :param val: The data byte to send to the LCD.
        """
        # RS pin = 1, write to data register
        self.RS.on()
        # Write the data
        self._write_byte(val)

    def write(self, s):
        """
        Display a string of characters on the LCD. This method writes
        each character of the string to the LCD, one by one.

        :param s: The string of characters to display on the LCD.
        """
        for c in s:
            self.data(ord(c))

    def move_to(self, line, column):
        """
        Move the cursor to a specified position on the LCD. The method
        supports two lines.

        :param line: The line number (1 or 2).
        :param column: The column number (1 to 20).
        """
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

    def custom_char(self, addr, charmap):
        """
        This method writes the pixel data for the custom character to one of
        the 8 available character generator RAM (CGRAM) locations.

        :param addr: The address (0 to 7) in the CGRAM to store the custom
                     character.
        :param charmap: A list of 8 bytes representing the custom character's
                        pixel pattern.

        .. note::
            Inspired by `peppe8o <https://peppe8o.com/download/micropython/LCD/lcd_api.py>`_
            and `MicrocontrollersLab <https://microcontrollerslab.com/i2c-lcd-esp32-esp8266-micropython-tutorial/>`_.
        """
        addr = addr & 0x07
        self.command(0x40 | (addr << 3))  # Set CG RAM address
        time.sleep_us(40)
        for i in range(8):
            self.data(charmap[i])
            time.sleep_us(40)
        self.command(0x80)  # Move to origin of DD RAM address


def demo():
    """
    Demonstrates the usage of the `LcdHd44780` class by initializing an
    LCD display, positioning text, and displaying a sample message.
    """
    # Four-data pins order:         [D4, D5, D6, D7]
    lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

    # Default LCD screen
    lcd.move_to(1, 3)
    lcd.write("Using LCD...")

    print("Start using HD44780-based LCD. Press `Ctrl+C` to stop")

    try:
        # Forever loop
        while True:
            pass

    except KeyboardInterrupt:
        # This part runs when Ctrl+C is pressed
        print("Program stopped. Exiting...")

        # Optional cleanup code
        lcd.command(0x01)  # Clear display


if __name__ == "__main__" :
    # Code that runs only if this script is executed directly
    demo()
