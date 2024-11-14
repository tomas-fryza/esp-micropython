from machine import SPI
from machine import Pin
from pcd8544 import PCD8544_FRAMEBUF
import time

"""
Philips PCD8544 / Nokia 5110 LCD pinout according to backside description and
this video tutorial https://educ8s.tv/raspberry-pi-pico-nokia5110-display-tutorial-using-circuitpython/,
https://github.com/educ8s/CircuitPython_PCD8544_Graphics
sadly, this is for CircuitPython and AdaFruit ecosystem

Library used: https://github.com/mcauser/micropython-pcd8544

This code is based on example.

|Pin|Name | Note                             | FireBeetle Pin  |
|--:|-----|----------------------------------|-----------|
| 1 | RST | External reset input, active low | 22: GP17  |
| 2 | CE  | Chip enable, active low          | 24: GP18  |
| 3 | D/C | Data high / Command low          | 21: GP16 |
| 4 | DIN | Serial data input                | 15: GP11 SPI:MOSI/TX |
| 5 | CLK | Serial clock, up to 4MHz         | 14: GP10 SPI:SCK |
| 6 | VCC | Supply voltage 2.7-3.3V          | 36: 3V3 |
| 7 | BL  | Backlight, active low            | Depends |
| 8 | GND | Ground                           | 38: GND |
"""

spi = SPI(1, baudrate=1_000_000, mosi=Pin(23), sck=Pin(18))
print(f"SPI configuration : {str(spi)}")

cs  = Pin(21)
dc  = Pin(16)
rst = Pin(22)
bli = Pin(15, Pin.OUT, value=0)

lcd = PCD8544_FRAMEBUF(spi, cs, dc, rst)

# Add some text at (x, y)
lcd.text("Nokia", 35, 0, 1)
lcd.text("ESP32", 35, 10, 1)

# Binary icon
icon = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0]]
# Copy icon to Nokia display position pixel-by-pixel
pos_x, pos_y = 50, 20
for j, row in enumerate(icon):
    for i, val in enumerate(row):
        lcd.pixel(i+pos_x, j+pos_y, val)

# Logo: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
lcd.fill_rect(0, 0, 32, 32, 1)
lcd.fill_rect(2, 2, 28, 28, 0)
lcd.vline(9, 8, 22, 1)
lcd.vline(16, 2, 22, 1)
lcd.vline(23, 8, 22, 1)
lcd.fill_rect(26, 24, 2, 4, 1)

# Finally update the Nokia display so the text is displayed
lcd.show()
time.sleep(1)
lcd.invert(1)
time.sleep(1)
lcd.invert(0)
time.sleep(1)

bli.value(1)
time.sleep(1)
lcd.power_off()
