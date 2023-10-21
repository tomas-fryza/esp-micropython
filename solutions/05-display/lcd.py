"""
MicroPython HD44780 character LCD controller

This module provides a simple interface to control character LCDs
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

import time
from machine import Pin

# Register Select pin, 0 - command, 1 - data
LCD_RS = Pin(26, Pin.OUT)

# Enable pin
LCD_E = Pin(25, Pin.OUT)
LCD_E.off()

# Four-bit data pins (D4, D5, D6, D7)
dataPins = (13, 10, 9, 27)
# Empty list for data pin objects
LCD_D = []
# Construct the list of data pin objects
for p in dataPins:
    LCD_D.append(Pin(p, Pin.OUT))


def lcd_set_data_bits(val):
    """Set four data pins according to the parameter val"""
    for i in range(4):
        # For each pin, set the value according to the corresponding bit
        LCD_D[i].value(val & (1 << (i + 4)))


def lcd_write_nibble(val):
    """Write upper nibbble of the value byte"""
    lcd_set_data_bits(val)
    LCD_E.on()
    time.sleep_us(1)
    LCD_E.off()


def lcd_write_byte(val):
    """Write a byte of value to the LCD controller"""
    lcd_write_nibble(val)  # Write upper nibble
    lcd_write_nibble(val << 4)  # Write lower nibble


def lcd_command(cmd):
    """Write a command to the LCD controller"""
    # RS pin = 0, write to command register
    LCD_RS.off()
    # Write the command
    lcd_write_byte(cmd)
    time.sleep_ms(2)


def lcd_data(val):
    """Write data to the LCD controller"""
    # RS pin = 1, write to data register
    LCD_RS.on()
    # Write the data
    lcd_write_byte(val)


def lcd_init():
    """Initialization sequence of HD44780"""
    # All commands will be sent
    LCD_RS.off()
    time.sleep_ms(20)
    lcd_write_nibble(0x30)
    time.sleep_ms(5)
    lcd_write_nibble(0x30)
    time.sleep_ms(1)
    lcd_write_nibble(0x30)
    time.sleep_ms(1)
    lcd_write_nibble(0x20)
    time.sleep_ms(1)
    lcd_command(0x28)  # 4-bit, 2 lines, 5x7 pixels
    lcd_command(0x06)  # Increment, no shift
    lcd_command(0x01)  # Clear display
    # lcd_command(0x0f)  # Display on, cursor on and blinking
    # lcd_command(0x0e)  # Display on, cursor on but not blinking
    lcd_command(0x0C)  # Display on, cursor off


def lcd_put_string(s):
    """Display a character string on the LCD"""
    for c in s:
        lcd_data(ord(c))


def lcd_cursor(line, column):
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
    lcd_command(cmd)


# Send initialization sequence
lcd_init()

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start using HD44780-based LCD...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        lcd_cursor(1, 3)
        lcd_put_string("Temperature")

        # Example how to put a numeric value to display
        TEMP = 23.25
        TEMP_STR = str(TEMP)
        TEMP_STR = TEMP_STR + chr(223) + "C"
        lcd_cursor(2, 5)
        lcd_put_string(TEMP_STR)

        time.sleep_ms(2000)
        lcd_command(0x01)  # Clear display
        time.sleep_ms(500)
except KeyboardInterrupt:
    lcd_command(0x01)  # Clear display
    print("Ctrl+C Pressed. Exiting...")
