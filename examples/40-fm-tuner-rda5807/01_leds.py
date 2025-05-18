from machine import Pin
import time

led_builtin = Pin(2, Pin.OUT)
led_builtin.off()
led_0 = Pin(19, Pin.OUT)
led_1 = Pin(18, Pin.OUT)
led_2 = Pin(5, Pin.OUT)
led_3 = Pin(17, Pin.OUT)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        led_0.value(not led_0.value())
        time.sleep(0.5)
        led_1.value(not led_1.value())
        time.sleep(0.5)
        led_2.value(not led_2.value())
        time.sleep(0.5)
        led_3.value(not led_3.value())
        time.sleep(0.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_0.off()
    led_1.off()
    led_2.off()
    led_3.off()
