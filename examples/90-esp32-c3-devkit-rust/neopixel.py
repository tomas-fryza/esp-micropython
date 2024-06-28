# ESP32-C3-DevKit-RUST
# https://github.com/esp-rs/esp-rust-board

from machine import Pin
import time
import sys
import neopixel
# https://docs.micropython.org/en/latest/library/neopixel.html

# On-board LED
led = Pin(7, Pin.OUT)
# One on-board WS2812 LED at pin2
neo = neopixel.NeoPixel(Pin(2), 1)

print(f"Start color gradient {led}")
print("Press `Ctrl+C` to stop")

# Forever loop
try:
    while True:
        led.on()
        
        # Set a color gradient
        for i in range(32):
            neo[0] = (0, 0, i*8)  # RGB
            neo.write()
            time.sleep_ms(100)

        led.off()
        time.sleep_ms(500)

# Ctrl+C
except KeyboardInterrupt:
    print("Program stopped")

    # Optional cleanup code
    led.off()
    neo[0] = (0, 0, 0)
    neo.write()

    # Stop program execution
    sys.exit(0)
