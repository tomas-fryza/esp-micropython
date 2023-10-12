"""Program 3-2: Non-blocking function `getkey()` detects
   key press. When a key is pressed, return the key id.
   If no key is pressed, return 0.
   
   Wiring of the keypad to FireBeetle ESP32 GPIO pins:
   row 1 - 19
   row 2 - 21
   row 3 - 22
   row 4 - 14
   
   col 1 - 12
   col 2 - 4
   col 3 - 16
   col 4 - 17
"""

import time
from machine import Pin

# Four pins connected to four rows
gpio_row = (19, 21, 22, 14)
# Four pins connected to four columns
gpio_col = (12, 4, 16, 17)

# Make a tuple of key Ids by row
keys = "123A", "456B", "789C", "*0#D"

# Empty list for row pin objects
rowPins = []
# Construct the list of row pin objects
for p in gpio_row:
    rowPins.append(Pin(p, Pin.IN))

# Empty list for column pin objects
colPins = []
# Construct the list of column pin objects
for p in gpio_col:
    colPins.append(Pin(p, Pin.IN, Pin.PULL_UP))

print(f"rows: {rowPins}")
print(f"cols: {colPins}")
print(keys)


def get_key():
    """Function to scan the keypad to see whether a key is pressed"""
    # Make all row pins output and set them low
    for row in rowPins:
        row.init(Pin.OUT)
        row.value(0)
        # Wait for signal to settle
        time.sleep_us(10)

        # Scan one column at a time
        for col in colPins:
            if col.value() == 0:  # If a column is low, a key is pressed
                row.init(Pin.IN)
                return keys[rowPins.index(row)][colPins.index(col)]
        row.init(Pin.IN)
        
    return 0  # If no key was pressed


# Code to test `get_key()` function
while True:
    key = get_key()
    
    if key != 0:
        print(key, end="")
        time.sleep_ms(10)
        while get_key() != 0:
            pass
        time.sleep_ms(10)
