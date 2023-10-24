"""
Breathing light

Example combines timer interrupts and PWM (Pulse Width Modulation)
for dimming an LED on an ESP32 using MicroPython. In this example,
a timer interrupt is used to periodically update the PWM duty cycle
to create a visual effect where the intensity or brightness of an LED,
smoothly and periodically increases and decreases in a manner that
resembles the rhythm of human breathing.

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


def timer0_handler(t):
    """Interrupt handler of Timer0"""
    global fade_direction

    # Read currect duty cycle in the range of 1 to 1024 (1-100%)
    # Note that, pulse width resolution is 10-bit only !
    current_duty = led_with_pwm.duty()

    # Increment or decrement the PWM duty cycle
    if fade_direction == 1:
        new_duty = current_duty + 10
    else:
        new_duty = current_duty - 10

    # Change the fade direction when the duty cycle reaches min or max
    if new_duty <= 0:
        new_duty = 0
        fade_direction = 1
    elif new_duty >= 800:
        new_duty = 800
        fade_direction = 0

    # Update the duty cycle in the range of 1 to 100
    led_with_pwm.duty(new_duty)
    # print(f"dir:{fade_direction}, cur:{current_duty}, new:{new_duty}")


# Attach PWM object on the LED pin and set frequency to 1 kHz
led_with_pwm = PWM(Pin(2), freq=1000)
led_with_pwm.duty(10)  # Approx. 1% duty cycle

# Define global variable
fade_direction = 1  # 1 - increasing brightness
                    # 0 - decreasing

# Create a Timer0 object for the interrupt
timer0 = Timer(0)
timer0.init(period=50, mode=Timer.PERIODIC, callback=timer0_handler)

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start *breathing* with LED...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")

    # Optional cleanup code
    timer0.deinit()        # Deinitialize the timer
    led_with_pwm.deinit()  # Deinitialized the PWM object
