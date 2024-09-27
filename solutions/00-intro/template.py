"""
MicroPython template

The script with a forever loop can be interrupted using
Ctrl+C.

Author: Tomas Fryza
Creation Date: 2023-09-21
Last Modified: 2024-09-27
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
    print("Program stopped. Exiting...")

    # Optional cleanup code

    # Stop program execution
    sys.exit(0)
