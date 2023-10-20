"""
Pulse Width Modulation (PWM)

MicroPython demonstrates the use of PWM to control the brightness
of an LED connected to an ESP32 microcontroller. PWM allows you
to vary the LED's brightness by changing the duty cycle of the
PWM signal.

See:
   https://www.upesy.com/blogs/tutorials/micropython-esp32-pwm-usage

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Use onboard LED or connect an external
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: uPesy, Tomas Fryza
Date: 2023-10-16
"""

from machine import Pin, PWM
import time

# Define the LED pin
led = Pin(2, Pin.OUT)
# Attach PWM object on the LED pin and set frequency to 1 kHz
led_with_pwm = PWM(led, freq=1000)

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        for duty in range(100):  # Duty from 0 to 100 %
            # Pulse width resolution is 10-bit only !
            led_with_pwm.duty(int(duty/100 * 1024))
            time.sleep_ms(15)
except KeyboardInterrupt:
    led_with_pwm.duty(0)
    print("Ctrl+C Pressed. Exiting...")
