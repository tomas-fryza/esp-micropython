"""
Custom characters for HD44780-based LCD

This script demonstrates how to create and use characters which are
not included in the CG ROM of HD44780 LCD controlller.

Components:
  - ESP32 microcontroller
  - LCD display:
     + RS: GPIO pin 26
     + R/W: GND
     + E: 25
     + D[7:4]: 27, 9, 10, 13

Author: Tomas Fryza
Creation Date: 2023-10-20
Last Modified: 2024-10-08
"""

from lcd_hd44780 import LcdHd44780
import sys

# Initialize LCD (four-data pins order is [D4, D5, D6, D7])
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

# Set custom character(s)
# https://www.quinapalus.com/hd44780udg.html
new_char = bytearray([0x4, 0xa, 0xa, 0xa, 0x11, 0x1f, 0xe, 0x00])
lcd.custom_char(0, new_char)

# Show new custom character(s)
lcd.move_to(2, 3)
lcd.write(chr(0))

# Example how to put a numeric value to display
TEMP = 23.25
TEMP_STR = str(TEMP)
TEMP_STR = TEMP_STR + chr(223) + "C"
lcd.move_to(2, 5)
lcd.write(TEMP_STR)

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

    # Stop program execution
    sys.exit(0)
