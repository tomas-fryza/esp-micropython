# https://www.upesy.com/blogs/tutorials/micropython-esp32-pwm-usage

from machine import Pin, PWM
import time

LED_BUITLTIN = 2 # For ESP32
pwm_led = PWM(Pin(LED_BUITLTIN, mode=Pin.OUT)) # Attach PWM object on the LED pin

# Settings
pwm_led.freq(1_000)


while True:
    for duty in range(0,1024, 5):
        pwm_led.duty(duty)
        time.sleep_ms(5)
    for duty in range(1023,-1, -5):
        pwm_led.duty(duty)
        time.sleep_ms(5)
