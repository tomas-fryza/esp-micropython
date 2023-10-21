"""
MicroPython Keypad Scanning

This MicroPython script scans a 4x4 keypad with rows as outputs
and columns as input pins with pull-up resistors. It detects
key presses and prints the pressed key.

Hardware Configuration:
  - Rows R1-R4: GPIO pins 19, 21, 22, 14 (set as Pin.OUT)
  - Columns C1-C4: GPIO pins 12, 4, 16, 17 (set as Pin.IN with Pin.PULL_UP)

Instructions:
1. Connect rows and columns of 4x4 key pad to GPIO pins
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-12
"""

from machine import Pin
import time

# Define the GPIO pins for rows (outputs) and columns (inputs with pull-ups)
row_pins = [Pin(pin, Pin.OUT) for pin in (19, 21, 22, 14)]
col_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in (12, 4, 16, 17)]

# Print info about pins
print(f"rows: {row_pins}")
print(f"cols: {col_pins}")

# Define the keypad matrix layout
keypad = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"],
]


def scan_keypad():
    key = None

    for row_num in range(len(row_pins)):
        # Set the current row LOW and the rest HIGH
        for r in range(len(row_pins)):
            row_pins[r].value(0 if r == row_num else 1)

        # Wait for signal to settle
        time.sleep_us(10)

        for col_num in range(len(col_pins)):
            # Read the column input
            if col_pins[col_num].value() == 0:
                key = keypad[row_num][col_num]
                while not col_pins[col_num].value():
                    pass  # Wait for key release

    return key


print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Press the button on the keypad...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        key_pressed = scan_keypad()
        if key_pressed:
            print(f"Key pressed: {key_pressed}")
            time.sleep_ms(10)  # Debounce delay
except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
