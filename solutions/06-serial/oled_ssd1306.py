import time
from machine import I2C
from machine import Pin

DEV_ADDR = 0x3c
WIDTH = 128
HEIGHT = 64
PAGE_NUM = 8
LOW_COLUMN_ADDR  = 0x00
HIGH_COLUMN_ADDR = 0x10
PAGE_ADDRESS = 0xb0


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

def send_data(data):
    i2c.writeto(DEV_ADDR, bytearray([0xc0, data]))

def send_command(cmd):
    i2c.writeto(DEV_ADDR, bytearray([0x80, cmd]))

def ssd1306_init():
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
        send_command(command)

def setRegion(x0, x1, y):
    send_command(0x21)
    send_command(x0)
    send_command(x1)
    send_command(0x22)
    send_command(y)
    send_command(y)


ssd1306_init()

FONT_TABLE = (
    (0x7e, 0x11, 0x11, 0x11, 0x7e, 0),  # A
    (0x7f, 0x49, 0x49, 0x49, 0x36, 0),  # B
    (0x3e, 0x41, 0x41, 0x41, 0x22, 0),  # C
    )

# for i in range(WIDTH - 3*6):
#     send_data(1)

for page in range(0, PAGE_NUM):
    send_command(PAGE_ADDRESS | page)
    send_command(LOW_COLUMN_ADDR | 0x0)
    for h_col in range(0, 8):
        send_command(HIGH_COLUMN_ADDR | h_col)
        for k in range(16):
            send_data(0x0)


#     for j in range(WIDTH / 8):
#         for k in range(4):
#             send_data(0xf0)

#         for k in range(4):
#             send_data(0x0f)

# setRegion(0, 20, 1)
send_command(PAGE_ADDRESS | 3)
send_command(LOW_COLUMN_ADDR | 0x0)
send_command(HIGH_COLUMN_ADDR | 2)
for j in range(3):
        for i in range(6):
            send_data(FONT_TABLE[j][i])
