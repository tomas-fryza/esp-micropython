from machine import Pin
import time

# Setup LED pin
led = Pin(2, Pin.OUT)

# Setup button pin with internal pull-up
button = Pin(27, Pin.IN, Pin.PULL_UP)

# Interrupt callback
def button_pressed(pin):
    # Debounce delay
    time.sleep_ms(20)
    if pin.value() == 0:  # Button pressed (active-low)
        led.value(not led.value())
        print(f"LED value: {led.value()}")

# Attach interrupt
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Main loop does nothing (LED controlled by interrupt)
while True:
    time.sleep(0.5)
