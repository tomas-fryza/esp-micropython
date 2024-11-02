"""
MicroPython template

The script with a forever loop can be interrupted using
Ctrl+C.

Author: Tomas Fryza

Creation date: 2023-09-21
Last modified: 2024-11-02
"""

import time

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
