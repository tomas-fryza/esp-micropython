"""
MicroPython HD44780 Character LCD Controller

This module provides a simple interface to control character LCDs
based on the HD44780 driver. It allows you to display text and
control the cursor position on the LCD screen.

Compatible with ESP32 boards and other MicroPython-supported hardware.

Hardware Configuration:
- Connect the LCD pins to your ESP32 as follows:
  - RS: GPIO pin 1
  - R/W: GND
  - E: 3
  - D4:7: 9, 27, 26, 25

Author(s): Shujen Chen et al. Raspberry Pi Pico Interfacing and
           Programming with MicroPython
           Tomas Fryza
Date: 2023-10-17
"""

import time
from machine import Pin

# Register Select pin, 0 - command, 1 - data
LCD_RS = Pin(1, Pin.OUT)

# Enable pin
LCD_E = Pin(3, Pin.OUT)
LCD_E.off()

# Four-bit data pins
dataPins = (9, 27, 26, 25)
# Empty list for data pin objects
LCD_D = []
# Construct the list of data pin objects
for p in dataPins:
    LCD_D.append(Pin(p, Pin.OUT))


def set_data_bits(val):
    """Set four data pins according to the parameter val"""
    for i in range(4):
        # For each pin, set the value according to the corresponding bit
        LCD_D[i].value(val & (1 << (i + 4)))


def write_nibble(val):
    """Write upper nibbble of the value byte"""
    set_data_bits(val)
    LCD_E.on()
    time.sleep_us(1)
    LCD_E.off()


def write_byte(val):
    """Write a byte of value to the LCD controller"""
    write_nibble(val)       # Write upper nibble
    write_nibble(val << 4)  # Write lower nibble


def command(cmd):
    """Write a command to the LCD controller"""
    # RS pin = 0, write to command register
    LCD_RS.off()
    # Write the command
    write_byte(cmd)
    time.sleep_ms(2)


def data(val):
    """Write data to the LCD controller"""
    # RS pin = 1, write to data register
    LCD_RS.on()
    # Write the data
    write_byte(val)


def init():
    """Initialization sequence of HD44780"""
    # All commands will be sent
    LCD_RS.off()
    time.sleep_ms(20)
    write_nibble(0x30)
    time.sleep_ms(5)
    write_nibble(0x30)
    time.sleep_ms(1)
    write_nibble(0x30)
    time.sleep_ms(1)
    write_nibble(0x20)
    time.sleep_ms(1)
    command(0x28)  # 4-bit, 2 lines, 5x7 pixels
    command(0x06)  # Increment, no shift
    command(0x01)  # Clear display
    # command(0x0f)  # Display on, cursor on and blinking
    # command(0x0e)  # Display on, cursor on but not blinking
    command(0x0c)  # Display on, cursor off


def put_string(s):
    """Display a character string on the LCD"""
    for c in s:
        data(ord(c))


def cursor(line, column):
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
    command(cmd)
