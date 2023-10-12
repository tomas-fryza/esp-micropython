"""Program 3-2: Non-blocking function `getkey()` detects
   key press. When a key is pressed, return the key id.
   If no key is pressed, return 0.
   
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

# Define the keypad matrix layout
# keys = [
#    ['1', '2', '3', 'A'],
#    ['4', '5', '6', 'B'],
#    ['7', '8', '9', 'C'],
#    ['*', '0', '#', 'D']
#]
# Make a tuple of keys by row
keys = "123A", "456B", "789C", "*0#D"

print(f"rows: {row_pins}")
print(f"cols: {col_pins}")
print(keys)


def scan_keypad():
    key = 0
    for row_num in range(4):
        # Set the current row LOW and the rest HIGH
        for r in range(4):
            row_pins[r].value(0 if r == row_num else 1)

        # Wait for signal to settle
        time.sleep_us(10)

        for col_num in range(4):
            # Read the column input
            if not col_pins[col_num].value():
                key = keys[row_num][col_num]
    return key


while True:
    key = scan_keypad()

    if key != 0:
        print(key, end="")
        # time.sleep_ms(10)
        while scan_keypad() != 0:
            pass
        # time.sleep_ms(10)
