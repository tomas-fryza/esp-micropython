"""


TODO: TEST IT !!!!



ST7796U TFT display demo for the LAFVIN Pico Development Kit.

TFT wiring built into the kit:
- GP2: SCK
- GP3: MOSI
- GP4: MISO (not used by this demo)
- GP5: CS
- GP6: DC
- GP7: RST
"""

from machine import Pin, SPI
from time import sleep_ms

WIDTH = 320
HEIGHT = 480

# RGB565 colours
BLACK = 0x0000
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
WHITE = 0xFFFF
YELLOW = 0xFFE0


class ST7796:
    def __init__(self):
        self.cs = Pin(5, Pin.OUT, value=1)
        self.dc = Pin(6, Pin.OUT, value=0)
        self.rst = Pin(7, Pin.OUT, value=1)

        self.spi = SPI(
            0,
            baudrate=20_000_000,
            polarity=0,
            phase=0,
            sck=Pin(2),
            mosi=Pin(3),
            miso=Pin(4),
        )

        self.reset()
        self.init_display()

    def command(self, command, data=None):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytes([command]))

        if data is not None:
            self.dc.on()
            self.spi.write(data)

        self.cs.on()

    def reset(self):
        self.rst.off()
        sleep_ms(20)
        self.rst.on()
        sleep_ms(150)

    def init_display(self):
        self.command(0x01)              # Software reset
        sleep_ms(150)
        self.command(0x11)              # Sleep out
        sleep_ms(120)

        self.command(0x36, b"\x48")     # Memory access control / rotation
        self.command(0x3A, b"\x55")     # RGB565 pixel format

        # ST7796 power, gamma, and display configuration
        self.command(0xF0, b"\xC3")
        self.command(0xF0, b"\x96")
        self.command(0xB4, b"\x01")
        self.command(0xB7, b"\xC6")
        self.command(0xC0, b"\x80\x45")
        self.command(0xC1, b"\x13")
        self.command(0xC2, b"\xA7")
        self.command(0xC5, b"\x0A")
        self.command(0xE8, b"\x40\x8A\x00\x00\x29\x19\xA5\x33")
        self.command(
            0xE0,
            b"\xD0\x08\x0F\x06\x06\x33\x30\x33\x47\x17\x13\x13\x2B\x31",
        )
        self.command(
            0xE1,
            b"\xD0\x0A\x11\x0B\x09\x07\x2F\x33\x47\x38\x15\x16\x2C\x32",
        )
        self.command(0xF0, b"\x3C")
        self.command(0xF0, b"\x69")

        self.command(0x21)              # Display inversion on
        self.command(0x29)              # Display on

    def set_window(self, x0, y0, x1, y1):
        self.command(0x2A, bytes([x0 >> 8, x0, x1 >> 8, x1]))
        self.command(0x2B, bytes([y0 >> 8, y0, y1 >> 8, y1]))
        self.command(0x2C)              # Start writing pixel data

    def fill(self, colour):
        self.set_window(0, 0, WIDTH - 1, HEIGHT - 1)

        pixel = bytes([colour >> 8, colour & 0xFF])
        line = pixel * WIDTH

        self.cs.off()
        self.dc.on()

        for _ in range(HEIGHT):
            self.spi.write(line)

        self.cs.on()


display = ST7796()

try:
    while True:
        display.fill(RED)
        sleep_ms(1000)

        display.fill(GREEN)
        sleep_ms(1000)

        display.fill(BLUE)
        sleep_ms(1000)

except KeyboardInterrupt:
    display.fill(BLACK)
    print("\nProgram stopped.")
