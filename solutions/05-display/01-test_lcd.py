"""
MicroPython script for HD44780-based LCD control

This script demonstrates the use of an HD44780-based LCD with MicroPython.
It initializes the LCD, creates a custom character (a thermometer icon),
and displays temperature information. The code runs in a loop until
interrupted by the user, and it provides a clean exit method.

Hardware Configuration:
- Connect HD44780-based LCD to your ESP32 as follows:
  - RS: GPIO pin 26
  - R/W: GND
  - E: 25
  - D7:4: 27, 9, 10, 13

Instructions:
1. Connect the LCD display to GPIO pins
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-20
"""

# Import necessary modules
from lcd_hd44780 import LcdHd44780
import time

# Initialize LCD and create custom character
# Four-data pins order: [D4, D5, D6, D7]
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

# Custom character(s)
# https://www.quinapalus.com/hd44780udg.html
thermometer = bytearray([0x4, 0xa, 0xa, 0xa, 0x11, 0x1f, 0xe, 0x00])
lcd.custom_char(0, thermometer)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start using HD44780-based LCD...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        lcd.move_to(1, 3)
        lcd.write("Temperature")
        lcd.move_to(2, 3)
        lcd.write(chr(0))  # Show custom character at addr 0
        lcd.move_to(2, 13)
        lcd.write(chr(0))

        # Example how to put a numeric value to display
        TEMP = 23.25
        TEMP_STR = str(TEMP)
        TEMP_STR = TEMP_STR + chr(223) + "C"
        lcd.move_to(2, 5)
        lcd.write(TEMP_STR)

        time.sleep_ms(2000)
        lcd.command(0x01)  # Clear display
        time.sleep_ms(500)

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")

    # Optional cleanup code
    lcd.command(0x01)  # Clear display
