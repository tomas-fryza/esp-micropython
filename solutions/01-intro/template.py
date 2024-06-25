from machine import Pin
import time
import sys

# On-board LED
led = Pin(2, Pin.OUT)

print(f"Start blinking {led}")
print("Press `Ctrl+C` to stop")

# Forever loop
try:
    while True:
        # led.value(not led.value())
        led.on()
        time.sleep_ms(500)
        led.off()
        time.sleep_ms(500)

# Ctrl+C
except KeyboardInterrupt:
    print("Program stopped")

    # Optional cleanup code
    led.off()

    # Stop program execution
    sys.exit(0)
