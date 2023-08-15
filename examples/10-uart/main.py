"""Example of internal UARTs.

Two UART instances are used independently: UART0 is used
for serial REPL and UART1 is used for serial data communication.
Note that, only serial transmitters are used here.

Inspired by:
    * https://forum.micropython.org/viewtopic.php?t=6076
    * https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/uart
"""

from machine import Pin
from machine import UART
from time import sleep_ms

# Status LED
led = Pin(2, Pin.OUT)

# Create two UART instances, one for REPL (TX=1, RX=3) and one
# for other serail communication
uart0 = UART(0, tx=1, rx=3)
uart0.init(baudrate=115200, bits=8, parity=None, stop=1)
uart1 = UART(1, tx=25, rx=26)
uart1.init(baudrate=9600, bits=8, parity=None, stop=1)

while True:
    led.on()
    # `uart0.write()` has the same output as `print()`
    uart0.write("uart0\r\n")
    print("Hi there")
    uart1.write("uart1\r\n")
    led.off()
    sleep_ms(1000)
