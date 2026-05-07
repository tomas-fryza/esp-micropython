"""
Sensors

Authors:
- Tomas Fryza

Creation date: 2025-01-23
Last modified: 2025-05-19
"""

# Micropython builtin modules
from machine import Pin
from machine import SoftI2C
import time

# External modules
import ssd1306             # OLED display
from bmp180 import BMP180  # Temperature/pressure meter


# Set your pins
PIN_LED = 2
PIN_PIR = 14


def init_display(i2c):
    """Initialize the OLED display and show startup screen."""
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.contrast(100)
    display.fill(0)
    return display


i2c = SoftI2C(sda=Pin(21), scl=Pin(22))

display = init_display(i2c)
bmp180 = BMP180(i2c)

led_builtin = Pin(PIN_LED, Pin.OUT)
pir = Pin(PIN_PIR, Pin.IN)

display.text("Sensors", 0, 5)
display.text("Temp. : ", 0, 16)
display.text("Press.: ", 0, 24)
display.text("Motion: ", 0, 32)

print("Press Ctrl+C to stop.")

try:
    # Forever loop
    while True:
        led_builtin.on()

        # x, y, width, height, color
        display.fill_rect(60, 16, 68, 24, 0)

        temperature = f"{bmp180.temperature:.1f} C"
        display.text(temperature, 60, 16, 1)

        pressure = f"{bmp180.pressure/100:.1f} hPa"
        display.text(pressure, 60, 24, 1)

        motion = str(pir.value())
        display.text(motion, 60, 32, 1)

        print(f"Temp.: {temperature} \tPress.: {pressure} \tMotion: {motion}")

        display.show()
        led_builtin.off()

        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_builtin.off()
    display.poweroff()
