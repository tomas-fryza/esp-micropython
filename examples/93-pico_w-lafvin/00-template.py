"""
MicroPython template

The script with a forever loop can be interrupted using
Ctrl+C.

Author: Tomas Fryza

Creation date: 2023-09-21
Last modified: 2026-08-07
"""

from time import sleep_ms

print("Press `Ctrl+C` to stop")
print()

try:
    # Forever loop
    while True:
        sleep_ms(500)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
