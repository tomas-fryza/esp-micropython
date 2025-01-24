# Example of Pico Inky Pack
#
# Instructions:
#
# 1. Download latest release of Pimoroni Pico Libraries
#    (such as pico-v1.23.0-1-pimoroni-micropython.uf2):
#
#    https://github.com/pimoroni/pimoroni-pico/releases
#
# 2. Connect the Pico Display, here `Pico Inky Pack`
# 3. Install the release
# 4. Program the example
#
# See also:
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md
# https://allrite.blog/2022/09/12/pico-rss-news-feed-reader/
# https://www.youtube.com/watch?v=ytnBCw5TO9s&ab_channel=MakingStuffwithChrisDeHut
# https://shkspr.mobi/blog/2024/06/displaying-a-qr-code-in-micropython-on-the-tildagon-badge/
# https://realpython.com/python-generate-qr-code/
# https://learn.pimoroni.com/article/getting-started-with-badger-2040

from picographics import PicoGraphics
from picographics import DISPLAY_INKY_PACK # 296x128 mono e-ink
from picographics import PEN_1BIT

badge = PicoGraphics(
    display=DISPLAY_INKY_PACK,
    pen_type=PEN_1BIT,
    rotate=0)

badge.set_pen(15)  # white
badge.clear()

badge.set_pen(0)  # black
badge.set_font("bitmap8")  # bitmap6, bitmap8, bitmap14_outline
badge.text("Tomas", 3, 3, scale=7)
# badge.text('Fryza', 150, 70, scale=2)
badge.text("Brno University of Technology", 32, 94, scale=1)

badge.line(20, 75, 185, 75)
badge.set_font("bitmap6")
badge.text("Czechia", 33, 102, scale=4)
# badge.text("Czechoslovakia", 2, 102, scale=4)

# QR code data (GitHub)
# https://github.com/tomas-fryza/
qr_code = [
    [1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,0,1,1,0,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,1,1],
    [0,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,1,1],
    [1,0,1,1,0,0,1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,1,1,0,1],
    [0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0],
    [1,1,1,1,0,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,0,0,0,0,1],
    [0,0,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,0,1,0,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,1],
    [0,0,0,0,0,1,0,1,0,1,1,1,1,0,1,1,0,0,0,1,1,1,0,0,0],
    [1,1,0,0,1,0,1,1,1,0,1,1,1,0,0,1,1,1,1,1,1,0,0,1,0],
    [0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,1,1,1,0,1,0,0,1,0,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,1,0,1,1,0,0,1,0,1,1,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,1,1,1,0,0,0,0],
    [1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,1,1,0],
    [1,0,1,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,1,1,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,0,0,1,0,0,1]]

# QR code data (LinkedIn)
# https://linkedin.com/in/tomas-fryza-0b008753/
qr_code = [
    [1,1,1,1,1,1,1,0,0,1,1,0,1,1,0,1,0,1,1,1,0,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,1,1,1,0,0,1,1,1,0,1,1,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,1,1,1,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,1,0,0,1,0,1,1,0,0,1,1,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
    [1,1,0,1,0,0,1,1,0,0,1,0,1,1,1,0,1,0,1,1,0,0,1,1,1,0,1,1,0],
    [1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1],
    [0,0,1,0,1,0,1,1,1,1,1,0,0,1,1,0,1,1,0,1,1,1,1,0,0,1,1,1,0],
    [0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1,1,0,1,1,0],
    [1,0,1,1,0,0,1,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,0,0,1,0,1,1],
    [1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,0,1,0,0,0,0,0],
    [1,0,0,1,0,0,1,1,1,1,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1],
    [1,1,0,1,0,0,0,0,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,0,1,0],
    [0,1,1,0,0,1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,1,0],
    [0,1,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,0,0,0,1,1,1,0,1,0,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,1,0,0,0,1,1],
    [0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,1,1],
    [1,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,1,1],
    [1,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,1,1,0,0,1,0,1,0,1,0,0,1,0],
    [1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0],
    [1,0,1,1,1,0,1,0,0,0,0,1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0],
    [1,0,1,1,1,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,1,1,1,0,1,0,0,1,1,0,1,1,1,1,0,1,0,0,1,0],
    [1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,1,1,1,1,0,0,1,0]]

pixel_size = 3
offset_x = 200
offset_y = 23

# Loop through the array
for row in range(len(qr_code)):
    for col in range(len(qr_code[0])):
        if qr_code[row][col] == 1:
            x = (col * pixel_size) + offset_x
            y = (row * pixel_size) + offset_y
            badge.rectangle(x, y, pixel_size, pixel_size)

badge.update()

# import time
# from pimoroni import Button

# button_a = Button(12)
# button_b = Button(13)
# button_c = Button(14)

# while True:
#     if button_a.read():
#         badge.line(10,50,286,50)
#         badge.update()
#     elif button_b.read():
#         badge.text("IEEE", 10, 70, 240, 4)
#         badge.update()
#     elif button_c.read():
#         badge.text("Brno University of Technology", 10, 118, 240, 1)
#         badge.update()
# 
#     time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
