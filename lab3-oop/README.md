# Lab 3: Object-oriented programming

* [Pre-Lab preparation](#preparation)
* [Part 1: Class and attributes](#part1)
* [Part 2: Button class](#part2)
* [Part 3: Inheritance and Led class](#part3)
* [Optional: PWM and LED](#part4)
* [Challenges](#challenges)
* [References](#references)

### Component list

* ESP32 board with pre-installed MicroPython firmware, USB cable
* Breadboard
* Push button
* Jumper wires

### Learning objectives

* Understand and implement classes, objects, attributes, and methods.
* Learn the key object-oriented programming (OOP) concepts like encapsulation, inheritance, and polymorphism.
* Define and use classes and objects in MicroPython.
* Apply OOP to manage hardware components like LEDs, buttons, or sensors.

<a name="preparation"></a>

## Pre-Lab preparation

1. Learn the basic principles of OOP, including encapsulating data and functions in classes, inheritance (sharing functions between classes), and polymorphism (modifying behavior in child classes).

2. Review how to use GPIO pins for input and output with MicroPython. How to configure a pin as an output to control an LED. How to configure a pin as an input (with or without pull-up resistors) to detect button presses.

<a name="part1"></a>

## Part 1: Class and attributes

1. Ensure your ESP32 board is connected to your computer via a USB cable. Open the Thonny IDE and set the interpreter to `ESP32`. You can click the red **Stop/Restart** button or press the on-board reset button if necessary to reset the board.

2. Test the following code and see how each **instance** has independent **attributes**.

   ```python
   class Dog:
       def __init__(self, name, breed):
           self.name = name    # instance attribute
           self.breed = breed  # instance attribute

   # Creating two objects
   dog1 = Dog("Buddy", "Golden Retriever")
   dog2 = Dog("Max", "Labrador")

   print(dog1.name)  # Buddy
   print(dog2.name)  # Max

   # Changing one instance does not affect the other
   dog1.name = "Charlie"
   print(dog1.name)  # Charlie
   print(dog2.name)  # Max
   ```

3. Test the **class attribute** which is shared across all objects. Here, changing `Dog.species` changes it for all objects.

   ```python
   class Dog:
       species = "Canis familiaris"  # class attribute

       def __init__(self, name):
           self.name = name          # instance attribute

   # Create objects
   dog1 = Dog("Rex")
   dog2 = Dog("Fido")

   # Accessing class attribute
   print(dog1.species)  # Canis familiaris
   print(dog2.species)  # Canis familiaris

   # Changing the class attribute
   Dog.species = "Domestic Dog"
   print(dog1.species)  # Domestic Dog
   print(dog2.species)  # Domestic Dog
   ```

   > **Note:** If you set an attribute with the same name on the object, it **shadows** the class attribute for that instance.
   >
   > ```python
   > # Override class attribute with instance attribute
   > dog1.species = "Wolf"
   > print(dog1.species)  # Wolf (from instance)
   > print(Dog.species)   # Canis familiaris (original class attribute)
   > ```

4. Test the following practical use of class attributes. Here, you can use class attributes to track shared information, like number of objects created.

   ```python
   class Dog:
       count = 0      # class attribute to count dogs
       all_dogs = []  # class attribute to track all instances

       def __init__(self, name):
           self.name = name
           Dog.count += 1
           Dog.all_dogs.append(self)

   dog1 = Dog("Luna")
   dog2 = Dog("Charlie")

   print("Number of dogs:", Dog.count)  # 2

   for dog in Dog.all_dogs:
       print(dog.name)
   ```

   Another example how to use class attributes:

   ```python
   class Dog:
       ...
       all_dogs = []  # class attribute to track all instances

       def __init__(self, name):
           ...
           Dog.all_dogs.append(self)

   ...
   for dog in Dog.all_dogs:
       print(dog.name)
   ```

<a name="part2"></a>

## Part 2: Button class

1. Use breadboard, jumper wires and connect one push button to ESP32 GPIO pin 27 in active-low way.

   ![firebeetle_pinout](../lab2-gpio/images/DFR0478_pinout3.png)

   > **Notes:**
   > * NC = Empty, Not Connected
   > * VCC = VCC (5V under USB power supply, Around 3.7V under 3.7V lipo battery power supply)
   > * Use pins A0, ..., A4 as input only
   > * Do not use In-Package Flash pins

2. Create a new file in Thonny and enter the following MicroPython code which is a **class definition** for the `Button` class. It is a blueprint for creating objects that represent a physical button with active-low logic connected to the ESP32 (or other microcontroller) GPIO pin.

   ```python
   from machine import Pin


   class Button:
       """A class to manage a button connected to a GPIO pin with internal pull-up resistor"""
       def __init__(self, pin_number):
           """Constructor with a specific GPIO pin and pull-up resistor."""
           self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

       def is_pressed(self):
           """Check if the button is currently pressed (active-low logic)."""
           return not self.button.value()  # Pressed button returns 1


   def demo():
       # Example usage of the Button class
       btn = Button(27)

       if btn.is_pressed():
           print(f"Button {btn} pressed...")
       else:
           print(f"Button {btn} released...")


   if __name__ == "__main__" :
       # Code that runs only if this script is executed directly
       demo()
   ```

   Some important parts:

      * The `__init__` method is the **constructor** that is automatically called when a new instance of the Button class is created.

      * Parameter (`pin_number`) represents the GPIO pin number where the button is connected.

      * In Python, `self` is a reference to the current instance of the class and is used to access instance variables and methods within the class.

      * The created object is stored in an instance variable (`self.button`), so it can be used in other methods of the class. Each instance of `Button` has its own `self.button`.

      * The `is_pressed()` method checks if the active-low button is being pressed. When the button is not pressed, the pin remains at logic 1 due to the pull-up resistor.

      * Note that `__name__` is a special built-in variable in Python that holds the name of the module (or script) currently being executed. If the script is being run directly (not imported), `__name__` will be set to `__main__`. The common usage of the `if __name__ == "__main__":` condition in Python is to allow a script to be used both as a **module** and as a **standalone program**. 

3. Save the file as `hw_config.py` in your local folder, run the code and test the button.

<a name="part3"></a>

## Part 3: Inheritance and Led class

Inheritance in Python is a core concept of object-oriented programming that allows a class (called a **child** or **subclass**) to inherit attributes and methods from another class (called a **parent** or **superclass**). This enables the child class to use or extend the functionality of the parent class without rewriting the same code.

1. Using the `Pin` class, create a subclass to complement the pin behavior for the LEDs. Use methods `self.on()`, `self.off()`, and `self.value()` inherited from the `Pin` class.

   ```python
   from machine import Pin
   import time

   ...

   class Led(Pin):  # Led is a subclass of Pin
       """A class to control an LED connected to a specified GPIO pin."""
       def __init__(self, pin_number):
           """Initialize the LED on a specific GPIO pin."""
           # Calls Parent's __init__ without needing `self`
           super().__init__(pin_number, Pin.OUT)

        def on(self):
            """Redefined method from Pin class"""
            self.led.value(1)

       def toggle(self):
           """Toggle the LED state."""
           # WRITE YOUR CODE HERE

       def blink(self, duration=0.5, times=5):
           """Make the LED blink a certain number of times."""
           # WRITE YOUR CODE HERE


   def demo():
       ...

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
   ```

   Some important parts:
      
      * Due to inheritance, the `Led` object is also a `Pin` object, and it can use any methods or attributes defined in the `Pin` class.

      * Method `super()` refers to the parent class (`Pin`) and calls its constructor. Python internally uses `self` to figure out the instance for which `super()` is being called, so there's no need to pass it explicitly.

      * Methods `self.on()` and `self.off()` rely on the `on()` and `off()` methods, which come from the `Pin` class. This shows how the `Led` class can use methods inherited from its parent class to implement higher-level functionality like blinking.

2.  Complete and test `toggle()` and `blink()` methods.

3. Write a program that toggles the LED state (on/off) every time the button is pressed.

<a name="part4"></a>

## Optional: PWM and LED

PWM (Pulse Width Modulation) is a technique used to control the amount of energy supplied to a device by rapidly switching the power supply on and off. The ratio of the time the signal is on (high) to the time it is off (low) is called the duty cycle, [expressed as a percentage](https://www.realdigital.org/doc/6136c69c3acc4bf52bc2653a067e36cc).

![pwm signal](images/pwm_signal.svg)

By adjusting the duty cycle, PWM can control the brightness of an LED. A higher duty cycle means the LED is on more often and appears brighter, while a lower duty cycle dims the LED. For example, a 50% duty cycle keeps the LED at half brightness, while 100% makes it fully bright.

![pwm led](images/pwm_led.png)

1. Using the `PWM` class from `machine` module, create a subclass to complement the pin behavior for the LEDs. Use methods `self.freq()` and `self.duty()` inherited from the `PWM` class.

   ```python
   from machine import Pin
   from machine import PWM
   import time

   ...

   class PwmLed(PWM):  # PwmLed is a subclass of PWM
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
           # WRITE YOUR CODE HERE

       def off(self):
           """Turn the LED off by setting the brightness to 0%."""
           # WRITE YOUR CODE HERE

       def fade_in(self, duration=1):
           """Fade in the LED by increasing brightness gradually in 100 steps."""
           step_duration = duration / 100
           for i in range(100):
               self.set_brightness(i)
               time.sleep(step_duration)

       def fade_out(self, duration=1):
           """Fade out the LED by decreasing brightness gradually in 100 steps."""
           # WRITE YOUR CODE HERE


   def demo():
       ...

       # Example of using the PwmLed class
       led = PwmLed(2)

       print("Fading in...")
       led.fade_in(duration=2)

       print("LED on at 10% brightness...")
       led.on(10)
       time.sleep(1)

       print("Turning LED off...")
       led.off()
       time.sleep(1)
   ```

   Some important parts:
      
      * The frequency `freq` can be a value between 0 and 78125. A frequency of 1000 Hz can be used to control the LED brightness.

      * The duty cycle can be a value between 0 and 1023. In which 1023 corresponds to 100% duty cycle (full brightness), and 0 corresponds to 0% duty cycle.

      * The `range()` function has the following syntax: `range(start, stop, step)`. By default, the `step` parameter is equal to 1.

2.  Complete and test `on()`, `off()`, and `fade_out()` methods.

3. To test if a class is a superclass or a subclass of another class in Python, you can use the built-in functions `issubclass()` and `isinstance()`.

   The `issubclass()` checks if a class is a subclass of another class. It returns `True` if the first argument is a subclass of the second. The `isinstance()` function checks if an object is an instance of a class or a subclass of that class. It returns `True` if the object is an instance of the specified class or any subclass thereof.

   ```python
       print("Testing class relationship...")
       print(issubclass(Led, PwmLed))
       print(isinstance(led, PWM))
   ```

<a name="challenges"></a>

## Challenges

1. Control the brightness of an LED using a button. Write a program that increases the brightness by 20% each time the button is pressed. Once it reaches 100%, the next press should reset it to 0%.

2. Create different blinking patterns for an LED based on button presses. Write a program that cycles through three different blinking patterns (e.g., fast, slow, and a double blink) each time the button is pressed.

<a name="references"></a>

## References

1. Fred's Cave. [MicroPython Class Inheritance](https://www.fredscave.com/31-micropython-class-inheritance.html)

2. MicroPython Documentation. [Pulse Width Modulation](https://docs.micropython.org/en/latest/esp32/tutorial/pwm.html)

3. RandomNerdTutorials.com. [ESP32/ESP8266 PWM with MicroPython – Dim LED](https://randomnerdtutorials.com/esp32-esp8266-pwm-micropython/)

4. Real Digital. [Project 4 A Pulse-Width Modulator IP Block](https://www.realdigital.org/doc/6136c69c3acc4bf52bc2653a067e36cc). Creating and programming a PWM circuit to control LED brightness
