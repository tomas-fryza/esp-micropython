"""
MicroPython template

The script with a forever loop can be interrupted using
Ctrl+C.

Author: Wokwi, Tomas Fryza
Date: 2023-09-21
"""

import time
import sys

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
