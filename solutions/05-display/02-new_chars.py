"""
Custom characters for HD44780-based CD

This script demonstrates how to create and use characters which are
not included in the CG ROM of HD44780 LCD controlller.

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
from lcd_hd44780 import LcdHd44780

# Initialize LCD (four-data pins order is [D4, D5, D6, D7])
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

# Set custom character(s)
# https://www.quinapalus.com/hd44780udg.html
new_char = bytearray([0x4, 0xa, 0xa, 0xa, 0x11, 0x1f, 0xe, 0x00])
lcd.custom_char(0, new_char)

# Show new custom character
lcd.move_to(2, 3)
lcd.write(chr(0))

# Example how to put a numeric value to display
TEMP = 23.25
TEMP_STR = str(TEMP)
TEMP_STR = TEMP_STR + chr(223) + "C"
lcd.move_to(2, 5)
lcd.write(TEMP_STR)

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
