"""
MicroPython HD44780 character LCD controller

This class provides a simple interface to control character LCDs
based on the HD44780 driver. It allows you to display text and
control the cursor position on the LCD screen.

Compatible with ESP32 boards and other MicroPython-supported hardware.

Hardware Configuration:
- Connect the LCD pins to your ESP32 as follows:
  - RS: GPIO pin 26
  - R/W: GND
  - E: 25
  - D7:4: 27, 9, 10, 13

Instructions:
1. Connect LCD display to GPIO pins
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author(s): Shujen Chen et al. Raspberry Pi Pico Interfacing and
           Programming with MicroPython
           Tomas Fryza
Date: 2023-10-17
"""

import time  # For time delays
from machine import Pin  # For GPIO control


class LcdHd44780:
    def __init__(self, rs, e, d):
        # Create a list of machine.Pin objects within the constructor
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
        # self.command(0x0f)  # Display on, cursor on and blinking
        # self.command(0x0e)  # Display on, cursor on but not blinking
        self.command(0x0C)  # Display on, cursor off

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

    def put_string(self, s):
        """Display a character string on the LCD"""
        for c in s:
            self.data(ord(c))

    def cursor(self, line, column):
        """Move cursor to a specified location of the display"""
        if line == 1:
            cmd = 0x80
        elif line == 2:
            cmd = 0xC0
        else:
            return

        if column < 1 or column > 20:
            return

        cmd += column - 1
        self.command(cmd)


# Example usage
# Four-bit data pins [D4, D5, D6, D7]
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start using HD44780-based LCD...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        lcd.cursor(1, 3)
        lcd.put_string("Temperature")

        # Example how to put a numeric value to display
        TEMP = 23.25
        TEMP_STR = str(TEMP)
        TEMP_STR = TEMP_STR + chr(223) + "C"
        lcd.cursor(2, 5)
        lcd.put_string(TEMP_STR)

        time.sleep_ms(2000)
        lcd.command(0x01)  # Clear display
        time.sleep_ms(500)
except KeyboardInterrupt:
    lcd.command(0x01)  # Clear display
    print("Ctrl+C Pressed. Exiting...")
