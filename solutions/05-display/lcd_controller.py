import time
from machine import Pin

# Enable pin
LCD_E = Pin(XXX, Pin.OUT)
LCD_E.off()

# Register Select pin, 1 - data, 0 - command
LCD_RS = Pin(XXX, Pin.OUT)

# Four-bit data pins
dataPins = (xx, xx, xx, xx, xx)
# Empty list for data pin objects
LCD_D = []
# Construct the list of dapa pin objects
for p in dataPins:
    LCD_D.append(Pin(p, Pin.OUT))


def lcd_set_data_bits(data):
    """Set eight data pins according to parameter data"""
    for i in range(4):
        # For each pin, set the value according to the corresponding bit
        LCD_D[i].value(data & (1 << (i + 4)))


def lcd_write_nibble(data):
    """Write upper nibbble of the data byte"""
    lcd_set_data_bits(data)
    LCD_E.on()
    time.sleep_us(1)
    LCD_E.off()


def lcd_write_byte(data):
    """Write a byte of data to the LCD controller"""
    lcd_write_nibble(data)       # Write upper nibble
    lcd_write_nibble(data << 4)  # Write lower nibble


def lcd_command(data):
    """Write a command to the LCD controller"""
    # RS pin = 0, write to command register
    LCD_RS.off()
    # Write the command
    lcd_write_byte(data)
    time.sleep_ms(2)


def lcd_data(data):
    """Write data to the LCD controller"""
    # RS pin = 1, write to data register
    LCD_RS.on()
    # Write the data
    lcd_write_byte(data)


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
    lcd_command(0x0f)  # Display on, cursor on and blinking


def lcd_put_string(s):
    """Display a character string on the LCD"""
    for c in s:
        lcd_data(ord(c))


def lcd_cursor(line, column):
    """Move cursor to a specified location of the display"""
    if line == 1:
        cmd = 0x80
    elif line == 2:
        cmd = 0xc0
    else
        return
    
    if column < 1 or column > 20:
        return
    
    cmd += column - 1
    lcd_command(cmd)


# Send initialization sequence
lcd_init()

while True:
    lcd_cursor(1, 3)
    lcd_put_string("Temperature")
    TEMP = 23.25
    TEMP_STR = str(TEMP)
    TEMP_STR = TEMP_STR + chr(223) + "C"
    lcd_cursor(2, 5)
    lcd_put_string(TEMP_STR)

    time.sleep_ms(1000)
    lcd_command(1)
    time.sleep_ms(1000)
