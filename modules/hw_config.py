"""
This module provides classes to manage common input/output components, 
such as buttons and LEDs, with support for PWM-based brightness control 
for LEDs. The classes allow for checking button states, toggling LEDs, 
blinking LEDs, and controlling brightness and fading effects using PWM.

Example
-------
.. code-block:: python

    from hw_config import Led

    led = Led(2)

    print("LED blinking...")
    led.blink(times=3)

    print("Toggling LED...")
    led.toggle()

    # Example of using the PwmLed class
    led = PwmLed(2)

    print("Fading in...")
    led.fade_in(duration=2)

Author
------
Tomas Fryza

Modification history
--------------------
- **2025-10-15** : Button redefined so that it inherits from Pin.
- **2024-11-11** : Added Sphinx-style comments for documentation.
- **2024-10-26** : Added `demo` method to demonstrate usage of the classes.
- **2024-09-28** : File created, initial release.
"""

from machine import Pin
from machine import PWM
import time


class Button(Pin):
    """
    A class to manage a button connected to a GPIO pin with a pull-up resistor.
    """

    def __init__(self, pin_number):
        """
        Initialize the button on a specific GPIO pin with a pull-up resistor.

        :param pin_number: GPIO pin number where the button is connected.
        """
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        """
        Check if the button is currently pressed using active-low logic.

        :return: `True` if the button is pressed; `False` otherwise.
        """
        if self.button.value() == 0:  # Pressed button returns 0
            return True
        return False


class Led(Pin):
    """
    A class to control an LED connected to a specified GPIO pin.
    """

    def __init__(self, pin_number):
        """
        Initialize the LED on a specific GPIO pin.

        :param pin_number: GPIO pin number where the LED is connected.
        """
        # Calls Parent's __init__ without needing `self`
        super().__init__(pin_number, Pin.OUT)

    def toggle(self):
        """
        Toggle the LED state between on and off.
        """
        self.value(not self.value())

    def blink(self, duration=0.5, times=5):
        """
        Blink the LED a specified number of times.

        :param duration: Duration in seconds for each on/off cycle.
                         Default is 0.5 seconds.
        :param times: Number of times the LED should blink. Default is 5.
        """
        for _ in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)


class PwmLed(PWM):
    """
    A class to control an LED using PWM, allowing for brightness
    adjustment, fading, and on/off control.
    """

    def __init__(self, pin_number, frequency=1000):
        """
        Initialize PWM on the specified pin with a given frequency,
        starting with LED off.

        :param pin_number: GPIO pin number where the LED is connected.
        :param frequency: PWM frequency for LED control. Default is 1000 Hz.
        """
        pin = Pin(pin_number, Pin.OUT)
        super().__init__(pin)
        self.freq(frequency)
        self.duty(0)
    
    def set_brightness(self, brightness):
        """
        Set the LED brightness using PWM.

        :param brightness: Brightness level as a percentage (0 to 100).
        """
        duty_cycle = int(brightness / 100 * 1023)  # Duty cycle 0 to 1023
        self.duty(duty_cycle)

    def on(self, brightness=100):
        """
        Turn the LED on by setting it to a specified brightness level.

        :param brightness: Brightness level as a percentage (0 to 100).
                           Default is 100%.
        """
        self.set_brightness(brightness)

    def off(self):
        """
        Turn the LED off by setting the brightness to 0.
        """
        self.set_brightness(0)

    def fade_in(self, duration=1):
        """
        Gradually increase the brightness to create a fade-in effect.

        :param duration: Total duration of the fade-in effect, in seconds.
                         Default is 1 second.
        """
        step_duration = duration / 100
        for i in range(100):
            self.set_brightness(i)
            time.sleep(step_duration)

    def fade_out(self, duration=1):
        """
        Gradually decrease the brightness to create a fade-out effect.

        :param duration: Total duration of the fade-out effect, in seconds.
                         Default is 1 second.
        """
        step_duration = duration / 100
        for i in range(100, -1, -1):  # -1 to reach fully off
            self.set_brightness(i)
            time.sleep(step_duration)


def demo():
    """
    Demonstrates usage of the `Button`, `Led`, and `PwmLed` classes.
    """
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


if __name__ == "__main__" :
    # Code that runs only if this script is executed directly
    demo()
