# Example of Pico Inky Pack
#
# Instructions:
#
# 1. Download latest release of Pimoroni Pico Libraries
#    (such as pico-v1.23.0-1-pimoroni-micropython.uf2):
#    https://github.com/pimoroni/pimoroni-pico/releases
#
# 2. Install the release
#
# 3. Connect the Pico Display, here `Pico Inky Pack`
#
# 4. Program the example
#
# See also:
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md
# https://allrite.blog/2022/09/12/pico-rss-news-feed-reader/
# https://www.youtube.com/watch?v=ytnBCw5TO9s&ab_channel=MakingStuffwithChrisDeHut
# https://shkspr.mobi/blog/2024/06/displaying-a-qr-code-in-micropython-on-the-tildagon-badge/
# https://realpython.com/python-generate-qr-code/

import time
from pimoroni import Button
from picographics import PicoGraphics
from picographics import DISPLAY_INKY_PACK # 296x128 mono e-ink
from picographics import PEN_1BIT


def clear():
    display.set_pen(WHITE)
    display.clear()
    display.update()


# Create a display object from the class and configure
display = PicoGraphics(
    display=DISPLAY_INKY_PACK,
    pen_type=PEN_1BIT,
    rotate=0)

# display.set_backlight(0.5)
display.set_font("bitmap8")  # bitmap6, bitmap8, bitmap14_outline

# button_a = Button(12)
# button_b = Button(13)
# button_c = Button(14)

WHITE = 15
BLACK = 0

clear()

display.set_pen(BLACK)
# text, x, y, wordwrap, scale
display.text("Tomas", 3, 3, 240, 8)
display.text('Fryza', 150, 67, 100, 2)
display.text("Brno University of Technology", 2, 94, 200, 1)
# display.line(10, 100, 286, 100)
display.set_font("bitmap6")
display.text("Czechia", 2, 102, 100, 4)
# display.text("Czechoslovakia", 2, 102, 296, 4)

# QR code data
qr_code = [
    [1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []]

# Size of each QR code pixel on the canvas
pixel_size = 5

# Offset size in pixels
offset_size = 46

# Calculate the offset to start drawing the QR code (centre it within the available space)
offset = 50 + offset_size

# Loop through the array
for row in range(9):
    for col in range(9):
        if qr_code[row][col] == 1:
            x = (col * pixel_size) + offset
            y = (row * pixel_size) + offset
            display.rectangle(x, y, pixel_size, pixel_size)
            print(x, y)

display.update()

# while True:
#     if button_a.read():
#         display.line(10,50,286,50)
#         display.update()
#     elif button_b.read():
#         display.text("IEEE", 10, 70, 240, 4)
#         display.update()
#     elif button_c.read():
#         display.text("Brno University of Technology", 10, 118, 240, 1)
#         display.update()
# 
#     time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
