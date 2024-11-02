"""
Class for HD44780-based LCD

This class provides a simple interface to control character LCDs
based on the HD44780 driver. It allows to display text, control
the cursor position on the LCD screen, and create the custom characters.

Components (if the script is executed directly):
- ESP32-based board
- LCD display:
   + RS: GPIO pin 26
   + R/W: GND
   + E: 25
   + D[7:4]: 27, 9, 10, 13

Authors:
- Shujen Chen et al. Raspberry Pi Pico Interfacing and Programming with MicroPython
- Tomas Fryza

Creation date: 2023-10-17
Last modified: 2024-11-02
"""

from machine import Pin
import time


class LcdHd44780:
    def __init__(self, rs, e, d):
        """Constructor. Set control and data pins of HD44780-based
        LCD and call the initialization sequence."""
        # Create machine.Pin objects within the constructor
        self.RS = Pin(rs, Pin.OUT)
        self.E = Pin(e, Pin.OUT)
        self.D = [Pin(pin_number, Pin.OUT) for pin_number in d]
        # Send initialization sequence
        self._init()

    def _init(self):
        """Initialization sequence of HD44780"""
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
        self._write_nibble(val)  # Write upper nibble
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

    def write(self, s):
        """Display a character string on the LCD"""
        for c in s:
            self.data(ord(c))

    def move_to(self, line, column):
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

    def custom_char(self, addr, charmap):
        """Write a character to one of the 8 CGRAM locations, available
        as chr(0) through chr(7).
        https://peppe8o.com/download/micropython/LCD/lcd_api.py
        https://microcontrollerslab.com/i2c-lcd-esp32-esp8266-micropython-tutorial/
        """
        addr = addr & 0x07
        self.command(0x40 | (addr << 3))  # Set CG RAM address
        time.sleep_us(40)
        for i in range(8):
            self.data(charmap[i])
            time.sleep_us(40)
        self.command(0x80)  # Move to origin of DD RAM address


# Code inside this block runs only if the script is executed directly
if __name__ == "__main__":

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
