# Lab 4: Timers

* [Pre-Lab preparation](#preparation)
* [Part 1: Interrupts](#part1)
* [Part 2: ESP32 timer overflows](#part2)
* [Part 3: Simple timer-controled tasks](#part3)
* [Challenges](#challenges)
* [References](#references)

### Component list
 
* ESP32 board with pre-installed MicroPython firmware, USB cable
* Breadboard
* 2 LEDs, 2 resistors
* Jumper wires

### Learning objectives

* Use internal microcontroller timers
* Combine different interrupts in MicroPython

<a name="preparation"></a>

## Pre-Lab preparation

1. Remind yourself how to write and run functions in MicroPython.

<a name="part1"></a>

## Part 1: Interrupts

Interrupts can be triggered by both internal and external devices within the microcontroller unit (MCU). It represents a signal **Interrupt request** sent to the processor by hardware or software, signifying an event that requires immediate attention. When an interrupt is triggered, the controller finishes executing the current instruction and proceeds to execute an **Interrupt Service Routine (ISR)** or Interrupt Handler. ISR tells the processor or controller what to do when the [interrupt occurs](https://www.tutorialspoint.com/embedded_systems/es_interrupts.htm). After the interrupt code is executed, the program continues exactly where it left off.

![interrupt_processing_flow](images/interrupt-processing-flow.jpg)

Interrupts can be set up for events such as a counter's value, a pin changing state, receiving data through serial communication, or when the Analog-to-Digital Converter has completed the conversion process.

<a name="part2"></a>

## Part 2: ESP32 timer overflows

A timer (or counter) is an integral hardware component in a microcontroller unit designed for measuring time-based events. Timers count from 0 to (2^n -1), where `n` being the number of bits of the counter. Thus, an 8-bit counter will count from 0 to 255, a 16-bit counter will count from 0 to 65535, and so on.

ESP32 has two timer groups, each group containing two 64-bit timers. Thus, there are four 64-bit timers in total, designated as Timer0, Timer1, and Timer2. They are all 64-bit generic timers based on 16-bit prescalers and 64-bit up/down counters which are capable of being auto-reloaded.

![esp32-timers](images/esp32-timers.png)

Prescalers help divide the base clock frequency. ESP32 generally has a base clock frequency of 80 MHz and it can be a bit too high. Having a 16-bit pre-scaler means that you can divide the base clock frequency by at least 2 and by as much as 65536. 80 MHz/65535 = 1.22 KHz. Now, this means that the frequency of a timer can be adjusted from 1.22 KHz to 80 MHz (of course in discrete steps). This wide range of frequency, along with the fact that these are 64-bit timers ensures that almost any interval is possible with ESP32 timers.

The timer interrupts are the best way to run non-blocking functions at a certain interval. For that, we can configure and attach a particular timer interrupt to a specific Interrupt Service Routine or ISR.

The MicroPython's `machine.Timer` class defines a baseline operation of initializing and executing a callback with a given period or once after some delay. This function is called automatically by the Timer0 interrupt every time the timer period elapses.

1. Ensure your ESP32 board is connected to your computer via a USB cable. Open the Thonny IDE and set the interpreter to `ESP32` or `ESP8266` (depending on your board). You can click the red **Stop/Restart** button or press the on-board reset button if necessary to reset the board.

2. Create a new file in Thonny and enter the following MicroPython code which is a template for the Timer usage.

   ```python
   from machine import Timer
   import sys


   def timer_handler(t):
       """Interrupt handler for Timer0.
          Args: t (Timer): The Timer object that triggered the interrupt.
       """
       print("Running...")


   # Create an object for 64-bit Timer0
   tim = Timer(0)
   # Initialize the timer to call the handler every 1000 s
   tim.init(period=1000,             # Timer period in milliseconds
            mode=Timer.PERIODIC,     # Set the timer to repeat after each period
            callback=timer_handler)  # Function to call when the timer triggers

   print("Timer started. Press `Ctrl+C` to stop")
   print(tim)

   try:
       # Forever loop to keep the program running
       # The timer runs independently in the background
       while True:
           pass

   except KeyboardInterrupt:
       # This part runs when Ctrl+C is pressed
       print("Program stopped. Exiting...")

       # Optional cleanup code
       tim.deinit()  # Stop the timer

       # Stop program execution
       sys.exit(0)
   ```

The init keyword arguments are:

   * `freq` is the timer frequency, in units of Hz
   * `period` is the timer period in milliseconds
   * `mode` can be `Timer.ONE_SHOT` or `Timer.PERIODIC`
   * `callback` is executed whenever a timer is triggered. The callback must take one argument, which is passed the Timer object.
   * Note that the timer is running even when program stopped. It must be deinicialized.

<!--
> **NOTE:** In MicroPython, the timer parameter of the `mycallback` function is a reference to the timer object that triggered the interrupt. This parameter allows you to identify which timer initiated the interrupt if your code works with multiple timers.
-->

3. Modify the template above, define a GPIO pin 2 and blink the on-board LED with a period of 1 sec. Try different Timer modes.

<a name="part3"></a>

## Part 3: Simple timer-controled tasks

Creating a time domain using the main timer interrupt of an ESP32 in MicroPython is a powerful way to precisely control timing for various tasks or applications. Use a global variable to identify time intervals and increment time variable(s) within a timer interrupt of an ESP32 in MicroPython. You can access these variables from both the timer interrupt and the main loop to perform tasks based on the elapsed time.

1. Use breadboard, jumper wires and connect two additional LEDs and resistors to ESP32 GPIO pins 25 and 26 in active-high way.

   ![firebeetle_pinout](../lab2-gpio/images/DFR0478_pinout3.png)

   > **Notes:**
   > * NC = Empty, Not Connected
   > * VCC = VCC (5V under USB power supply, Around 3.7V under 3.7V lipo battery power supply)
   > * Use pins A0, ..., A4 as input only
   > * Do not use In-Package Flash pins

2. Create a new source file in your local folder and use the following code to control a single task by Timer interrupt.

   ```python
   from machine import Pin
   from machine import Timer
   import sys

   # Initialize counter(s) for different task(s)
   task_a_counter = 0

   # Define the intervals in terms of timer ticks (e.g., ticks every 100ms)
   task_a_interval = 5   # Task A runs every 500ms (5 ticks)


   def timer_handler(t):
      """Interrupt handler for Timer0."""
      global task_a_counter

      # Increment counter(s)
      task_a_counter += 1


   def task_a():
      """Task A: Runs every 100ms"""
      print("Task A executed: LED")
      led.value(not led.value())


   # Create and initialize Timer0
   tim = Timer(0)
   tim.init(period=100,
            mode=Timer.PERIODIC,
            callback=timer_handler)

   # Create object for LED
   led = Pin(2, mode=Pin.OUT)

   print("Timer started. Press `Ctrl+C` to stop")

   try:
      # Forever loop
      while True:
         # Task A (every 100ms)
         if task_a_counter >= task_a_interval:
               task_a_counter = 0  # Reset the counter
               task_a()

   except KeyboardInterrupt:
      # This part runs when Ctrl+C is pressed
      print("Program stopped. Exiting...")

      # Optional cleanup code
      tim.deinit()  # Stop the timer
      led.off()

      # Stop program execution
      sys.exit(0)
   ```

3. Extend the previous code to continuously blink all three LEDs (onboard + external ones) at different periods. Let each LED is controlled by a single task.

<!--
<a name="part3"></a>

## Part 3: PWM and LED dimming

**Pulse Width Modulation** (PWM) changes the average power delivered from a signal by chopping the square wave signal into discrete parts. It is not an actual continuous signal. Instead, a periodic digital signal's ON, and OFF duration is modulated to reduce the effective voltage/power output. For example, if a microcontroller's GPIO outputs 3.3V in digital output while generating a PWM signal of [50% duty cycle](https://makeabilitylab.github.io/physcomp/esp32/led-fade.html) from the pin, it will output an effective voltage of approximately 1.65V, i.e., 3.3/2.

   ![pwm_duty-princip](images/pwm_princip.png)

   ![pwm_duty-cycles](images/pwm_duty-cycles.png)

The PWM class is written to provide pulse width modulation in MicroPython supported boards. This class can be imported into a MicroPython script using the following statements. After importing, an object has to be instantiated from the PWM class.

   ```python
   from machine import PWM
   pwm_object = PWM(pin, freq=frequency, duty=duty_cycle)
   ```

1. Create a new source file, save it as `03-pwm.py` in your local folder, and write the code to change a duty cycles of onboard LED (`Pin(2)`) within a `for` cycle from 0 to 1024 (10-bit resolution) in forever loop. To deinitialize PWM object, use `deinit()` method.

   ```python
   from machine import Pin, PWM
   import time

   # Attach PWM object on the LED pin and set frequency to 1 kHz
   led_with_pwm = PWM(Pin(2), freq=1000)
   led_with_pwm.duty(10)  # Approx. 1% duty cycle of 10-bit range

   try:
       while True:
           for duty in range(0, 1024, 5):  # 0, 5, 10, ..., 1020, 0, ...
               # Pulse width resolution is 10-bit only !
               led_with_pwm.duty(duty)
               time.sleep_ms(10)

   except KeyboardInterrupt:
       print("Ctrl+C Pressed. Exiting...")

       # Optional cleanup code
       led_with_pwm.deinit()  # Deinitialized the PWM object
   ```

2. Modify the duty cycle of one LED within the Timer0 interrupt handler instead of the main loop. This approach allows you to independently control the duty cycles of multiple PWM signals.

   Program a *Breathing light* application. It is a visual effect where the intensity or brightness of an LED, smoothly and periodically increases and decreases in a manner that resembles the rhythm of human breathing. This effect is often used in various electronic and lighting applications to create visually appealing and calming effects.

   ```python
   from machine import Pin, Timer, PWM


   def timer0_handler(t):
       """Interrupt handler of Timer0"""
       global fade_direction

       # Read currect duty cycle in the range of 1 to 1024 (1-100%)
       # Note that, pulse width resolution is 10-bit only !
       current_duty = led_with_pwm.duty()


       # COMPLETE THE CODE: Increment or decrement the PWM duty cycle


       # Update the duty cycle in the range of 1 to 1024
       led_with_pwm.duty(new_duty)


   # Attach PWM object on the LED pin and set frequency to 1 kHz
   led_with_pwm = PWM(Pin(2), freq=1000)
   led_with_pwm.duty(10)  # Approx. 1% duty cycle

   # Define global variable
   fade_direction = 1  # 1 - increasing brightness
                       # 0 - decreasing

   # Create a Timer0 object for the interrupt
   timer0 = Timer(0)
   timer0.init(period=50, mode=Timer.PERIODIC, callback=timer0_handler)

   try:
       while True:
           pass

   except KeyboardInterrupt:
       print("Ctrl+C Pressed. Exiting...")

       # Optional cleanup code
       timer0.deinit()        # Deinitialize the timer
       led_with_pwm.deinit()  # Deinitialized the PWM object
   ```
-->



<a name="challenges"></a>

## Challenges

1. xxx


1. To combine timers and PWM in MicroPython on an ESP32, create a smooth fading effect using an RGB LED or two-colour LED. By controlling the intensity of the red, green, and blue components, you can achieve various colors and dynamic color transitions. Timers will be used to control the PWM signals for each color component.

<a name="references"></a>

## References

1. MicroPython documentation. [class Timer -- control hardware timers](https://docs.micropython.org/en/latest/library/machine.Timer.html)

2. Physical Computing. [Lesson 3: Fading an LED with PWM](https://makeabilitylab.github.io/physcomp/esp32/led-fade.html)

3. Nikhil Agnihotri. [MicroPython -- Generating PWM on ESP8266 and ESP32](https://www.engineersgarage.com/micropython-esp8266-esp32-pwm-led-fading/)

4. MicroPython documentation. [class PWM -- pulse width modulation](https://docs.micropython.org/en/latest/library/machine.PWM.html)
