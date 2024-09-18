# https://github.com/pimoroni/pimoroni-pico/releases
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md
# https://allrite.blog/2022/09/12/pico-rss-news-feed-reader/
# https://www.youtube.com/watch?v=ytnBCw5TO9s&ab_channel=MakingStuffwithChrisDeHut


import time
from pimoroni import Button
from picographics import PicoGraphics
from picographics import DISPLAY_INKY_PACK # 296x128 mono e-ink
from picographics import PEN_1BIT

# Create a display object from the class and configure
display = PicoGraphics(display=DISPLAY_INKY_PACK,
                       pen_type=PEN_1BIT,
                       rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

WHITE = 15
BLACK = 0


def clear():
    display.set_pen(WHITE)
    display.clear()
    display.update()


clear()

display.set_pen(BLACK)
display.text("Tomas", 5, 5, 240, 7)
# display.line(5, 56, 291, 56, 1)
display.text("Fryza", 219, 40, 60, 2)
display.text("Brno Univ. of Technology", 61, 80, 240, 2)
# display.line(10, 100, 286, 100)
display.set_font("bitmap6")
display.text("Czechia", 152, 100, 100, 4)
# display.text("Czechoslovakia", 2, 100, 296, 4)

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
