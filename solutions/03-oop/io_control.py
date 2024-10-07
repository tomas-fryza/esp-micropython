"""
GPIO classes for common components

This file defines classes to manage common GPIO components like
buttons and LEDs, including PWM control for adjustable LED
brightness.

Components:
  - ESP32 microcontroller
  - Button connected to GPIO pin 27
  - LED connected to GPIO pin 2 (on-board)

Author: Tomas Fryza
Creation Date: 2024-09-28
Last Modified: 2024-10-07
"""

from machine import Pin
from machine import PWM
import time


class Button:
    """
    A class to manage a button connected to a GPIO pin with pull-up resistor.
    """

    def __init__(self, pin_number):
        """Initialize the button on a specific GPIO pin with
           pull-up resistor."""
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        """Check if the button is currently pressed (active-low logic)."""
        if self.button.value() == 0:  # Pressed button returns 0
            return True
        return False


class Led(Pin):
    """
    A class to control an LED connected to a specified GPIO pin.
    """

    def __init__(self, pin_number):
        """Initialize the LED on a specific GPIO pin."""
        # Calls Parent's __init__ without needing `self`
        super().__init__(pin_number, Pin.OUT)

    def toggle(self):
        """Toggle the LED state."""
        self.value(not self.value())

    def blink(self, duration=0.5, times=5):
        """Make the LED blink a certain number of times."""
        for i in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)


class PwmLed(PWM):
    """
    A class to control an LED using PWM, allowing for brightness adjustment, fading, and on/off control.
    """
    def __init__(self, pin_number, frequency=1000):
        """Initialize PWM on the given pin with a default frequency and
           starts with a duty cycle of 0 (LED off)."""
        pin = Pin(pin_number, Pin.OUT)
        super().__init__(pin)
        self.freq(frequency)
        self.duty(0)
    
    def set_brightness(self, brightness):
        """Set the LED brightness using PWM (0 to 100%)."""
        duty_cycle = int(brightness / 100 * 1023)  # Duty cycle 0 to 1023
        self.duty(duty_cycle)

    def on(self, brightness=100):
        """Turn the LED on by setting the brightness to 100%."""
        self.set_brightness(brightness)

    def off(self):
        """Turn the LED off by setting the brightness to 0%."""
        self.set_brightness(0)

    def fade_in(self, duration=1):
        """Fade in the LED by increasing brightness gradually."""
        step_duration = duration / 100
        for i in range(100):
            self.set_brightness(i)
            time.sleep(step_duration)

    def fade_out(self, duration=1):
        """Fade out the LED by decreasing brightness gradually."""
        step_duration = duration / 100
        for i in range(100, -1, -1):  # -1 to reach fully off
            self.set_brightness(i)
            time.sleep(step_duration)


# Code inside this block runs only if the script is executed directly
if __name__ == "__main__" :

    # Example usage of the Button class
    btn = Button(27)

    if btn.is_pressed():
        print(f"Button {btn} pressed...")
    else:
        print(f"Button {btn} released...")


    # Example of using the Led class
    led = Led(2)

    print("LED blinking...")
    led.blink(times=3)

    print("Toggling LED...")
    led.toggle()
    time.sleep(1)

    print("Turning LED off...")
    led.off()
    time.sleep(1)


    # Example of using the PwmLed class
    led = PwmLed(2)

    print("Fading in...")
    led.fade_in(duration=2)

    print("Fading out...")
    led.fade_out(duration=2)
    time.sleep(1)

    print("LED on at 10% brightness...")
    led.on(10)
    time.sleep(1)
    print("LED on at 40% brightness...")
    led.on(40)
    time.sleep(1)
    print("LED on at 100% brightness...")
    led.on(100)
    time.sleep(1)

    print("Turning LED off...")
    led.off()
    time.sleep(1)

    print("Testing class relationship...")
    print(issubclass(Led, Pin))
    print(issubclass(PwmLed, Led))
    print(issubclass(Led, PwmLed))
    print(isinstance(led, PWM))
