"""UART example.

TBD.

Inspired by:
     TBD
"""

from machine import UART

uart = UART(0, baudrate=115200, tx=1, rx=3)

uart.write("test")

while True:
    pass
