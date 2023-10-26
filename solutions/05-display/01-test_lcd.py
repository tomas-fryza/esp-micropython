"""
MicroPython script for HD44780-based LCD control

This script demonstrates the use of an HD44780-based LCD with
MicroPython. It initializes the LCD and write static text to
the display.

Hardware Configuration:
- Connect HD44780-based LCD to your ESP32 as follows:
  - RS: GPIO pin 26
  - R/W: GND
  - E: 25
  - D7:4: 27, 9, 10, 13

Instructions:
1. Connect the LCD display to GPIO pins
2. Run the script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-20
"""

# Import necessary module(s)
# From `lcd_hd4480.py` file import class `LcdHd4480`
from lcd_hd44780 import LcdHd44780

# Initialize LCD (four-data pins order is [D4, D5, D6, D7])
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

# Default screen
lcd.move_to(1, 3)
lcd.write("Using LCD...")

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start using HD44780-based LCD...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")

    # Optional cleanup code
    lcd.command(0x01)  # Clear display
