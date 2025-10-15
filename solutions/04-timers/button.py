"""
Example of ESP32 Button interrupt

Author: Tomas Fryza

Creation date: 2025-10-15
Last modified: 2025-10-15
"""

from machine import Pin
from hw_config import Button
from hw_config import Led


# Define the callback function to handle the interrupt
def button_handler(pin):
   led.toggle()


# Define the button pin (GPIO 27) and attach an interrupt
btn = Button(27)
btn.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

led = Led(2)

print("Press the button")

try:
    while True:
        pass

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    btn.irq(handler=None)  # Deinit the interrupt
    led.off()
