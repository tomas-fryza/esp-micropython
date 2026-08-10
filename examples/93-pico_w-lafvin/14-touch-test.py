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

from lafvin_tft import GT911
from time import sleep_ms

touch = GT911()

print("Touch the screen. Press `Ctrl+C` to stop")
print()

try:
    while True:
        for touch_id, x, y, size in touch.touches():
            print(
                "id={}, x={}, y={}, size={}".format(
                    touch_id, x, y, size,
                )
            )
        sleep_ms(50)

except KeyboardInterrupt:
    print()
    print("Program stopped. Exiting...")
