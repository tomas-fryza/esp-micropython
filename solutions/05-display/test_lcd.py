"""
Example of HD44780-based LCD

This script demonstrates the use of an HD44780-based LCD with
MicroPython. It initializes the LCD and write static text to
the display.

Author: Tomas Fryza
Creation Date: 2023-10-20
Last Modified: 2024-10-08
"""

from lcd_hd44780 import LcdHd44780
import sys

# Initialize LCD (four-data pins order is [D4, D5, D6, D7])
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

    # Stop program execution
    sys.exit(0)
