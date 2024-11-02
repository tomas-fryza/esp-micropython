"""
Example of HD44780-based LCD

This script demonstrates the use of an HD44780-based LCD with
MicroPython. It initializes the LCD and write static text to
the display.

Components:
- ESP32-based board
- LCD display:
   + RS: GPIO pin 26
   + R/W: GND
   + E: 25
   + D[7:4]: 27, 9, 10, 13

Author: Tomas Fryza

Creation date: 2023-10-20
Last modified: 2024-11-02
"""

from lcd_hd44780 import LcdHd44780

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
