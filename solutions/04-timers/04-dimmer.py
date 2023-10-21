"""
LED dimmer

Example combines timer interrupts and PWM (Pulse Width Modulation)
for dimming an LED on an ESP32 using MicroPython. In this example,
a timer interrupt is used to periodically update the PWM duty cycle
to create a fading effect on the LED.

Hardware Configuration:
  - LED: GPIO pin 2 (onboard)

Instructions:
1. Use onboard LED or connect an external
2. Run the current script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-20
"""

from machine import Pin, Timer, PWM

# Define the LED pin
led = Pin(2, Pin.OUT)
# Attach PWM object on the LED pin and set frequency to 1 kHz
led_with_pwm = PWM(led, freq=1000)
led_with_pwm.duty(10)  # approx. 1% duty cycle

# Timer interrupt global variables
timer_counter = 0
fade_direction = 1  # 1 for increasing brightness, -1 for decreasing


def irq_timer0(t):
    global fade_direction
    global timer_counter

    # Read currect duty cycle in the range of 1 to 1024 (1-100%)
    # Note that, pulse width resolution is 10-bit only !
    current_duty = led_with_pwm.duty()

    # Increment or decrement the PWM duty cycle
    if fade_direction == 1:
        new_duty = current_duty + 10
    else:
        new_duty = current_duty - 10

    # Change the fade direction when the duty cycle reaches min or max
    if new_duty < 0:
        new_duty = 0
        fade_direction = 1
    elif new_duty > 800:
        new_duty = 800
        fade_direction = 0

    # Update the duty cycle in the range of 1 to 100
    led_with_pwm.duty(new_duty)
    print(f"dir:{fade_direction}, cur:{current_duty}, new:{new_duty}")

    timer_counter += 1


# Create a Timer0 object for the interrupt
timer0 = Timer(0)
timer0.init(mode=Timer.PERIODIC, period=15, callback=irq_timer0)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print(f"Start dimming LED {led} in both directions...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        pass
except KeyboardInterrupt:
    timer0.deinit()       # Deinitialize the timer
    led_with_pwm.duty(0)  # Turn off the LED
    print("Ctrl+C Pressed. Exiting...")
