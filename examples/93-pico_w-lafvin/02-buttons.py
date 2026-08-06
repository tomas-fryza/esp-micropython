"""
Button state monitoring

Components:
- Raspberry Pi Pico + LAFVIN board
- LED1: GPIO pin 16
- LED2: GPIO pin 17
- Button connected to GPIO pin 14
- Button connected to GPIO pin 15
- Buzzer connected to GPIO pin 13

Author: Tomas Fryza

Creation date: 2023-10-12
Last modified: 2026-07-21
"""

from machine import Pin
from time import sleep_ms

led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)
btn1 = Pin(14, Pin.IN, Pin.PULL_UP)
btn2 = Pin(15, Pin.IN, Pin.PULL_UP)
buzz = Pin(13, Pin.OUT)
buzz.off()

print(f"Press buttons {btn1}, {btn2} to blink or `Ctrl+C` to stop")
print()

try:
    # Forever loop
    while True:
        if btn1.value() == 0:
            led1.on()
            buzz.on()
            print("Button K2 pressed")
            sleep_ms(10)
            led1.off()
            buzz.off()
            sleep_ms(990)
    
        if btn2.value() == 0:
            led2.on()
            print("Button K1 pressed")
            sleep_ms(100)
            led2.off()
            sleep_ms(900)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led1.off()
    led2.off()
    buzz.off()
