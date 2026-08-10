"""
ST7796U display and GT911 touch driver for the LAFVIN Pico kit.

Display: SPI0, GP2..GP7
- GP2: SCK
- GP3: MOSI
- GP4: MISO
- GP5: CS
- GP6: DC
- GP7: RST

Touch: I2C0, SDA GP8, SCL GP9

Authors:
- https://coxxect.blogspot.com/2025/02/use-st7796-spi-lcd-on.html
- Codex (OpenAI)
- Tomas Fryza

References
- https://lafvin-pico-development-kit.readthedocs.io/en/latest/about_this_kit.html
- https://docs.micropython.org/en/v1.22.0/library/micropython.html
- https://www.crystalfontz.com/controllers/uploaded/GT911ProgrammingGuide.pdf

Creation date: 2026-08-07
Last modified: 2026-08-10
"""

from machine import Pin, SPI, I2C
from time import sleep_ms
import micropython

WIDTH = 320
HEIGHT = 480

# RGB565 colours
BLACK = 0x0000
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
WHITE = 0xFFFF
YELLOW = 0xFFE0

# 5x7 bitmap font.  Each tuple contains five vertical columns; the least
# significant bit is the top pixel.  Lowercase glyphs are included so labels
# and simple status messages can be shown without a framebuffer.
FONT_5X7 = {
    " ": (0x00, 0x00, 0x00, 0x00, 0x00),
    "!": (0x00, 0x00, 0x5F, 0x00, 0x00),
    "?": (0x02, 0x01, 0x51, 0x09, 0x06),
    ".": (0x00, 0x60, 0x60, 0x00, 0x00),
    ",": (0x00, 0x80, 0x60, 0x00, 0x00),
    ":": (0x00, 0x36, 0x36, 0x00, 0x00),
    ";": (0x00, 0x80, 0x56, 0x00, 0x00),
    "-": (0x08, 0x08, 0x08, 0x08, 0x08),
    "_": (0x80, 0x80, 0x80, 0x80, 0x80),
    "+": (0x08, 0x08, 0x3E, 0x08, 0x08),
    "/": (0x20, 0x10, 0x08, 0x04, 0x02),
    "0": (0x3E, 0x51, 0x49, 0x45, 0x3E),
    "1": (0x00, 0x42, 0x7F, 0x40, 0x00),
    "2": (0x42, 0x61, 0x51, 0x49, 0x46),
    "3": (0x21, 0x41, 0x45, 0x4B, 0x31),
    "4": (0x18, 0x14, 0x12, 0x7F, 0x10),
    "5": (0x27, 0x45, 0x45, 0x45, 0x39),
    "6": (0x3C, 0x4A, 0x49, 0x49, 0x30),
    "7": (0x01, 0x71, 0x09, 0x05, 0x03),
    "8": (0x36, 0x49, 0x49, 0x49, 0x36),
    "9": (0x06, 0x49, 0x49, 0x29, 0x1E),
    "A": (0x7E, 0x11, 0x11, 0x11, 0x7E),
    "B": (0x7F, 0x49, 0x49, 0x49, 0x36),
    "C": (0x3E, 0x41, 0x41, 0x41, 0x22),
    "D": (0x7F, 0x41, 0x41, 0x22, 0x1C),
    "E": (0x7F, 0x49, 0x49, 0x49, 0x41),
    "F": (0x7F, 0x09, 0x09, 0x09, 0x01),
    "G": (0x3E, 0x41, 0x49, 0x49, 0x7A),
    "H": (0x7F, 0x08, 0x08, 0x08, 0x7F),
    "I": (0x00, 0x41, 0x7F, 0x41, 0x00),
    "J": (0x20, 0x40, 0x41, 0x3F, 0x01),
    "K": (0x7F, 0x08, 0x14, 0x22, 0x41),
    "L": (0x7F, 0x40, 0x40, 0x40, 0x40),
    "M": (0x7F, 0x02, 0x0C, 0x02, 0x7F),
    "N": (0x7F, 0x04, 0x08, 0x10, 0x7F),
    "O": (0x3E, 0x41, 0x41, 0x41, 0x3E),
    "P": (0x7F, 0x09, 0x09, 0x09, 0x06),
    "Q": (0x3E, 0x41, 0x51, 0x21, 0x5E),
    "R": (0x7F, 0x09, 0x19, 0x29, 0x46),
    "S": (0x46, 0x49, 0x49, 0x49, 0x31),
    "T": (0x01, 0x01, 0x7F, 0x01, 0x01),
    "U": (0x3F, 0x40, 0x40, 0x40, 0x3F),
    "V": (0x1F, 0x20, 0x40, 0x20, 0x1F),
    "W": (0x3F, 0x40, 0x38, 0x40, 0x3F),
    "X": (0x63, 0x14, 0x08, 0x14, 0x63),
    "Y": (0x07, 0x08, 0x70, 0x08, 0x07),
    "Z": (0x61, 0x51, 0x49, 0x45, 0x43),
    "a": (0x20, 0x54, 0x54, 0x54, 0x78),
    "b": (0x7F, 0x48, 0x44, 0x44, 0x38),
    "c": (0x38, 0x44, 0x44, 0x44, 0x20),
    "d": (0x38, 0x44, 0x44, 0x48, 0x7F),
    "e": (0x38, 0x54, 0x54, 0x54, 0x18),
    "f": (0x08, 0x7E, 0x09, 0x01, 0x02),
    "g": (0x0C, 0x52, 0x52, 0x52, 0x3E),
    "h": (0x7F, 0x08, 0x04, 0x04, 0x78),
    "i": (0x00, 0x44, 0x7D, 0x40, 0x00),
    "j": (0x20, 0x40, 0x44, 0x3D, 0x00),
    "k": (0x7F, 0x10, 0x28, 0x44, 0x00),
    "l": (0x00, 0x41, 0x7F, 0x40, 0x00),
    "m": (0x7C, 0x04, 0x18, 0x04, 0x78),
    "n": (0x7C, 0x08, 0x04, 0x04, 0x78),
    "o": (0x38, 0x44, 0x44, 0x44, 0x38),
    "p": (0x7C, 0x14, 0x14, 0x14, 0x08),
    "q": (0x08, 0x14, 0x14, 0x18, 0x7C),
    "r": (0x7C, 0x08, 0x04, 0x04, 0x08),
    "s": (0x48, 0x54, 0x54, 0x54, 0x20),
    "t": (0x04, 0x3F, 0x44, 0x40, 0x20),
    "u": (0x3C, 0x40, 0x40, 0x20, 0x7C),
    "v": (0x1C, 0x20, 0x40, 0x20, 0x1C),
    "w": (0x3C, 0x40, 0x30, 0x40, 0x3C),
    "x": (0x44, 0x28, 0x10, 0x28, 0x44),
    "y": (0x0C, 0x50, 0x50, 0x50, 0x3C),
    "z": (0x44, 0x64, 0x54, 0x4C, 0x44),
}


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
        # Each coordinate is sent as two bytes.  Mask the low byte because
        # `bytes()` only accepts values in the range 0..255 (e.g. y1 is 479).
        self.command(0x2A, bytes([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        self.command(0x2B, bytes([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        self.command(0x2C)              # Start writing pixel data

    def fill(self, colour):
        self.set_window(0, 0, WIDTH - 1, HEIGHT - 1)

        pixel = bytes([colour >> 8, colour & 0xFF])
        line = pixel * WIDTH

        self.cs.off()
        self.dc.on()

        try:
            for _ in range(HEIGHT):
                self.spi.write(line)
        finally:
            self.cs.on()

    def clear(self, colour=BLACK):
        self.fill(colour)

    def fill_rect(self, x, y, width, height, colour):
        # Clip the rectangle to the visible display area.
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(WIDTH - 1, x + width - 1)
        y1 = min(HEIGHT - 1, y + height - 1)

        if x0 > x1 or y0 > y1:
            return

        self.set_window(x0, y0, x1, y1)
        pixel = bytes([colour >> 8, colour & 0xFF])
        line = pixel * (x1 - x0 + 1)

        self.cs.off()
        self.dc.on()

        try:
            for _ in range(y1 - y0 + 1):
                self.spi.write(line)
        finally:
            self.cs.on()

    def pixel(self, x, y, colour):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.fill_rect(x, y, 1, 1, colour)

    def hline(self, x, y, length, colour):
        self.fill_rect(x, y, length, 1, colour)

    def vline(self, x, y, length, colour):
        self.fill_rect(x, y, 1, length, colour)

    def rect(self, x, y, width, height, colour):
        if width <= 0 or height <= 0:
            return

        self.hline(x, y, width, colour)
        self.hline(x, y + height - 1, width, colour)
        self.vline(x, y, height, colour)
        self.vline(x + width - 1, y, height, colour)

    def line(self, x0, y0, x1, y1, colour):
        # Bresenham line algorithm.
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:
            self.pixel(x0, y0, colour)

            if x0 == x1 and y0 == y1:
                break

            twice_error = 2 * error

            if twice_error >= dy:
                error += dy
                x0 += sx

            if twice_error <= dx:
                error += dx
                y0 += sy

    def char(self, character, x, y, colour, background=None, scale=1):
        """Draw one 5x7 character at x, y."""
        if not character or scale < 1:
            return

        glyph = FONT_5X7.get(character[0], FONT_5X7["?"])

        if background is not None:
            self.fill_rect(x, y, 5 * scale, 7 * scale, background)

        for column, bits in enumerate(glyph):
            for row in range(7):
                if bits & (1 << row):
                    self.fill_rect(
                        x + column * scale,
                        y + row * scale,
                        scale,
                        scale,
                        colour,
                    )

    def text(self, value, x, y, colour, background=None, scale=1,
             spacing=1, line_spacing=1):
        """Draw text. Newlines are supported; unsupported glyphs use '?'."""
        if scale < 1:
            return

        start_x = x
        character_step = (5 + spacing) * scale
        line_step = (7 + line_spacing) * scale

        for character in str(value):
            if character == "\n":
                x = start_x
                y += line_step
            else:
                self.char(character, x, y, colour, background, scale)
                x += character_step

    def text_size(self, value, scale=1, spacing=1, line_spacing=1):
        """Return the width and height in pixels required by text()."""
        if scale < 1 or not value:
            return 0, 0

        lines = str(value).split("\n")
        longest_line = max(len(line) for line in lines)
        width = max(0, (longest_line * (5 + spacing) - spacing) * scale)
        height = (len(lines) * 7 + (len(lines) - 1) * line_spacing) * scale
        return width, height

    def vut_logo(self, x, y, colour=RED, background=WHITE):
        """Draw the VUT Brno-inspired logo at x, y."""
        scale = 3  # Scale the original 32x32 design

        self.fill_rect(x, y, 32 * scale, 32 * scale, colour)
        self.fill_rect(
            x + 5 * scale, y + 5 * scale,
            10 * scale, 4 * scale,
            background,
        )
        self.fill_rect(
            x + 15 * scale, y + 9 * scale,
            12 * scale, 3 * scale,
            background,
        )
        self.fill_rect(
            x + 15 * scale, y + 12 * scale,
            4 * scale, 15 * scale,
            background,
        )
        self.fill_rect(
            x + 19 * scale, y + 12 * scale,
            scale, scale,
            background,
        )


class GT911:
    ADDRESS = 0x5D
    STATUS_REGISTER = 0x814E
    POINT_DATA_REGISTER = 0x814F

    def __init__(self):
        self.i2c = I2C(
            0,
            sda=Pin(8),
            scl=Pin(9),
            freq=400_000,
        )

        addresses = self.i2c.scan()
        # print("I2C devices:", [hex(address) for address in addresses])

        if self.ADDRESS not in addresses:
            raise OSError("GT911 touch controller not found at 0x5D")

    def read_register(self, register, length):
        # GT911 uses 16-bit register addresses.
        self.i2c.writeto(
            self.ADDRESS,
            bytes([register >> 8, register & 0xFF]),
            False,
        )
        return self.i2c.readfrom(self.ADDRESS, length)

    def write_register(self, register, data):
        self.i2c.writeto(
            self.ADDRESS,
            bytes([register >> 8, register & 0xFF]) + data,
        )

    def touches(self):
        """Return [(id, x, y, size), ...]; an empty list means no touch."""
        status = self.read_register(self.STATUS_REGISTER, 1)[0]

        if not (status & 0x80):
            return []

        count = status & 0x0F
        if count == 0 or count > 5:
            self.write_register(self.STATUS_REGISTER, b"\x00")
            return []

        data = self.read_register(self.POINT_DATA_REGISTER, count * 8)
        points = []

        for index in range(count):
            offset = index * 8
            touch_id = data[offset] & 0x0F
            x = data[offset + 1] | (data[offset + 2] << 8)
            y = data[offset + 3] | (data[offset + 4] << 8)
            size = data[offset + 5] | (data[offset + 6] << 8)
            points.append((touch_id, x, y, size))

        # Acknowledge the data so GT911 can report the next touch.
        self.write_register(self.STATUS_REGISTER, b"\x00")
        return points


if __name__ == "__main__":
    # Run only when this file is executed directly.

    display = ST7796()
    touch = GT911()

    display.fill(RED)
    sleep_ms(500)

    display.fill(GREEN)
    sleep_ms(500)

    display.fill(BLUE)
    sleep_ms(500)

    display.clear(BLACK)
    display.vut_logo(0, 0)
    display.text("MicroPython", 110, 20, WHITE, scale=3)
    display.text("VUT Brno", 110, 50, WHITE, scale=2)
    display.text("Radioelectronics", 110, 70, WHITE, scale=2)
    display.line(0, 95, 320, 95, RED)

    display.fill_rect(20, 120, 280, 40, BLUE)
    display.rect(160, 140, 100, 40, WHITE)

    display.text("Hello World", 20, 200, WHITE)
    display.text("Hello World", 20, 240, WHITE, scale=2)
    display.text("Hello World", 20, 280, GREEN, scale=3)
    display.text("Hello World", 20, 320, RED, scale=4)
    display.text("Hello World", 20, 360, WHITE, background=RED, scale=5)
    display.text("Hello World", 20, 400, YELLOW, scale=6)

    print("Touch the screen. Press `Ctrl+C` to stop")
    print()

    try:
        while True:
            points = touch.touches()

            for touch_id, x, y, size in points:
                print(
                    "touch id={}, x={}, y={}, size={}".format(
                        touch_id, x, y, size,
                    )
                )

            sleep_ms(50)

    except KeyboardInterrupt:
        # Do not allow a second Ctrl+C to interrupt the full-screen cleanup.
        micropython.kbd_intr(-1)

        try:
            display.clear(BLACK)
        finally:
            micropython.kbd_intr(3)  # Restore normal Ctrl+C handling.

        print()
        print("Program stopped. Exiting...")

