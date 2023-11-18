#
# NOTE: In Thonny IDE, enable `\r` and ANSI-color support in menu:
#
#   Tools > Options... > Shell > Terminal emulation (...)
#

import time

values = range(0, 100)
for i in values:
    print(f"Complete: {i}%", end="\r")
    time.sleep(.025)

print("\rComplete: 100%")

symbols = ["/", "-", "\\", "|"]
for i in range(10):
    for symbol in symbols:
        print(f"Processing... {symbol}", end="\r")
        time.sleep(.05)
print("Processing... Done")

# ANSI Escape Sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
print("This is \x1b[1;32mGreen and Bold\x1b[0m text")
print("\x1b[1;31m[ERROR]\x1b[0m End of file")
