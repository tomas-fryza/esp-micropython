from machine import Pin
from machine import PWM
import time


class Button:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return not self.pin.value()  # Active-low button


class Led(Pin):
    """
    A class to control an LED connected to a specified GPIO pin.

    Methods:
    - toggle(): Toggles the LED state.
    - blink(duration=0.5, times=5): Blinks the LED for a given duration and number of times.
    """

    def __init__(self, pin_number):
        """Initialize the LED on a specific GPIO pin."""
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
    def __init__(self, pin_number, frequency=1000):
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


# __name__ is a special built-in variable in Python that holds the
# name of the module (or script) currently being executed. If the
# script is being run directly, __name__ will be set to "__main__".

if __name__ == "__main__" :

    # Example of using the Led class
    led = Led(2)

    print("LED blinking...")
    led.blink(times=3)

    print("Toggling LED...")
    led.toggle()
    time.sleep(1)

    print("Turning LED off...")
    led.off()


    # Example of using the PwmLed class
    led = PwmLed(2)

    print("Fading in...")
    led.fade_in(duration=2)

    print("Fading out...")
    led.fade_out(duration=2)
    time.sleep(1)

    print("LED on at 25% brightness...")
    led.on(25)
    time.sleep(2)

    print("Turning LED off...")
    led.off()


    # Example usage of the Button class
    btn = Button(27)

    if btn.is_pressed():
        led.on()
    else:
        led.off()

    print(issubclass(Led, PwmLed))
    print(issubclass(PwmLed, Led))
