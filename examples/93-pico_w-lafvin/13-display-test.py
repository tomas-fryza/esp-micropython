"""
ST7796U TFT display test

Components:
- Raspberry Pi Pico + LAFVIN board
- ST7796U 320x480 TFT display
- SPI0: GP2-GP7

Uses:
- lafvin_tft.ST7796

Authors:
- Codex (OpenAI)
- Tomas Fryza

Creation date: 2026-08-10
Last modified: 2026-08-10
"""

import micropython
from time import sleep_ms
from lafvin_tft import ST7796, BLACK, WHITE, RED, YELLOW, GREEN

display = ST7796()

display.clear(BLACK)
display.vut_logo(20, 20, RED)
display.text("MicroPython", 130, 30, WHITE, scale=3)
display.text("VUT Brno", 130, 60, YELLOW, scale=2)
display.text("Radioelectronics", 130, 85, GREEN, scale=2)

print("Press `Ctrl+C` to stop")

try:
    while True:
        sleep_ms(1000)

except KeyboardInterrupt:
    # Do not allow a second Ctrl+C to interrupt the full-screen cleanup.
    micropython.kbd_intr(-1)

    try:
        display.clear(BLACK)
    finally:
        micropython.kbd_intr(3)  # Restore normal Ctrl+C handling.

    print()
    print("Program stopped. Exiting...")
