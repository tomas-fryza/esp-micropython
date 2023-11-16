import time
import framebuf
from machine import I2C
from machine import Pin


class SSD1306(framebuf.FrameBuffer):
    DEV_ADDR = 0x3c
    WIDTH = 128
    HEIGHT = 64
    PAGE_NUM = HEIGHT // 8
    WHITE = 1
    BLACK = 0

    def __init__(self):
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
        self.ssd1306_init()

        self.buffer = bytearray(self.WIDTH * self.PAGE_NUM)
        super().__init__(self.buffer, self.WIDTH, self.HEIGHT, framebuf.MONO_VLSB)

    def send_command(self, cmd):
        self.i2c.writeto(self.DEV_ADDR, bytearray([0x80, cmd]))

    def send_data(self, data):
        self.i2c.writeto(self.DEV_ADDR, bytearray([0xc0, data]))

    def ssd1306_init(self):
        INIT_SEQ = (
            0xae,        # Turn off oled panel
            0x00,        # Set low column address
            0x10,        # Set high column address
            0x40,        # Set start line address
            0x20, 0x02,  # Page addressing mode
            0xc8,        # Top-down segment (4th segment)
            0x81,        # Set contrast control register
            0xcf, 0xa1,
            0xa6,        # Set normal display
            0xa8,
            0x3f,
            0xd3,
            0x00,
            0xd5,
            0x80,
            0xd9,
            0xf1, 0xda,
            0x12, 0xdb,
            0x40, 0x8d,
            0x14,
            0xaf         # Turn on oled panel
        )
        time.sleep_ms(100)

        for command in INIT_SEQ:
            self.send_command(command)

    def setRegion(self, x0, x1, y):
        self.send_command(0x21)
        self.send_command(x0)
        self.send_command(x1)
        self.send_command(0x22)
        self.send_command(y)
        self.send_command(y)

    def flush(self):
        for page in range(self.PAGE_NUM):
            print(f"Updating pages {page}")
            self.setRegion(0, self.WIDTH-1, page)
            for column in range(self.WIDTH):
                print(f"{column} ", end="")
                self.send_data(self.buffer[page*self.WIDTH + column])


if __name__ == "__main__":
    oled = SSD1306()

    # Write message
    oled.fill(oled.BLACK)
    oled.text("Hello from", 0, 5, oled.WHITE)
    oled.text("MicroPython!", 20, 16, oled.WHITE)

    x = 10
    y = 30
    w = oled.WIDTH - 20
    h = oled.HEIGHT - 30
    c = oled.WHITE

    while h > 0:
        oled.fill_rect(x, y, w, h, c)
        x += 2
        y += 2
        w -= 4
        h -= 4
        c = oled.WHITE if c == oled.BLACK else oled.BLACK

    oled.flush()
