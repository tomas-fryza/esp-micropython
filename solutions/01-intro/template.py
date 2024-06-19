import sys
from machine import Pin
from time import sleep_ms


def main():
    led.value(not led.value())
    sleep_ms(500)


# Check the LED pin on your board (usually GPIO 2)
led = Pin(2, Pin.OUT)

print(f"Start blinking {led}")
print("Press `Ctrl+C` to stop")

# Forever loop
while True:
    try:
        main()

    # Ctrl+C
    except KeyboardInterrupt:
        print("Program stopped")
        sys.exit(0)
