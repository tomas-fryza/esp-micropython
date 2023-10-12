"""Program 3-2: Non-blocking function `get_key()` detects
   key press. When a key is pressed, return the key Id.
   If no key is pressed, return None.
   
   Wiring of the keypad to FireBeetle ESP32 GPIO pins:
   row 1 - 19  OUTs
   row 2 - 21
   row 3 - 22
   row 4 - 14
   
   col 1 - 12  INs
   col 2 - 4
   col 3 - 16
   col 4 - 17
"""

from machine import Pin
import time

# Define the GPIO pins for rows (outputs) and columns (inputs with pull-ups)
row_pins = [Pin(pin, Pin.OUT) for pin in (19, 21, 22, 14)]
col_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in (12, 4, 16, 17)]

# Make a tuple of keys and dfine the keypad matrix layout
keys = "123A", "456B", "789C", "*0#D"

print(f"rows: {row_pins}")
print(f"cols: {col_pins}")
print(keys)


def get_key():
    key = None  # Default key Id

    for row_num in range(4):
        # Set the current row LOW and the rest HIGH
        for r in range(4):
            row_pins[r].value(0 if r == row_num else 1)

        # Wait for signal to settle
        time.sleep_us(10)

        for col_num in range(4):
            # Read the column input
            if col_pins[col_num].value() == 0:
                # If a column is low, a key is pressed                
                key = keys[row_num][col_num]
    
    return key


# Code to test `get_key()` function
while True:
    key = get_key()

    if key != None:
        print(key, end="")
        time.sleep_ms(10)

        while get_key() != None:
            pass
        time.sleep_ms(10)
