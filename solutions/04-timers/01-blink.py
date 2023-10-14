"""
With this script, the built-in blue LED of the ESP32 starts
blinking every second, without using loops
"""
from machine import Timer, Pin

pin_led = Pin(2, mode=Pin.OUT)
timer_0 = Timer(0)  # Between 0-3 for ESP32


def interruption_handler(timer):
    pin_led.value(not pin_led.value())


if __name__ == "__main__":
    timer_0.init(mode=Timer.PERIODIC, period=1000, callback=interruption_handler)
