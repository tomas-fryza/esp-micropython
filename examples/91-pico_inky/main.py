# https://github.com/pimoroni/pimoroni-pico/releases
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md
# https://allrite.blog/2022/09/12/pico-rss-news-feed-reader/
# https://www.youtube.com/watch?v=ytnBCw5TO9s&ab_channel=MakingStuffwithChrisDeHut

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
display.set_font("bitmap8")

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

WHITE = 15
BLACK = 0

clear()

display.set_pen(BLACK)
display.text("Tomas", 3, 3, 240, 8)
display.text('"Snowman" Fryza', 35, 67, 200, 2)
display.text("Brno University of Technology", 152, 94, 200, 1)
# display.line(10, 100, 286, 100)
display.set_font("bitmap6")
display.text("Czechia", 155, 102, 100, 4)
# display.text("Czechoslovakia", 2, 102, 296, 4)

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
