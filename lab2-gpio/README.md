# Lab 2: Control of GPIO pins

* [Pre-Lab preparation](#preparation)
* [Part 1: Blink example](#part1)
* [Part 2: ESP32 pinout and Breadboard](#part2)
* [Part 3: LEDs and push buttons](#part3)
* [Challenges](#challenges)
* [References](#references)

### Component list

* ESP32 board with pre-installed MicroPython firmware, USB cable
* Breadboard
* 2 LEDs, 2 resistors
* Push button
* Jumper wires

### Learning objectives

* Use a breadboard for prototyping.
* Configure input/output pins of ESP32.
* Understand the distinction between active-low and active-high connections.
* Utilize basic I/O components, such as buttons and LEDs in MicroPython.

<a name="preparation"></a>

## Pre-Lab preparation

1. Ensure you have a basic understanding of electronic components, including resistors, LEDs, buttons, as well as concepts like voltage, current, and digital input/output.

2. Review how to write and run MicroPython code on the ESP32 microcontroller. This includes understanding variables, loops, functions, and how to handle input/outputs (I/O) operations.

<a name="part1"></a>

## Part 1: Blink example

1. Connect the ESP32: Ensure your ESP32 board is connected to your computer via a USB cable. Open the Thonny IDE and set the interpreter to `ESP32`. You can click the red **Stop/Restart** button or press the on-board reset button if necessary to reset your board.

   ![interpreter](../lab1-python/images/select_interpreter2.png)

   > **Note:** Your USB port can be different.

2. Using Thonny REPL: Open the Thonny shell (REPL) to interact with the ESP32. You can now send Python commands directly to the board. The ESP32 has an onboard LED typically connected to GPIO pin 2. To turn the LED on and off, type the following in the REPL:

   ```python
   from machine import Pin
   led = Pin(2, Pin.OUT)

   led.on()
   led.off()

   led.value(1)
   led.value()

   led.value(not led.value())
   ```

   The `machine` module in MicroPython provides access to low-level hardware functions, such as controlling GPIO pins on the ESP32 board. You can import the entire module or specific parts (classes) of it by:
   
   ```python
   from machine import Pin
   ```

3. Create a New File: Create a new file in Thonny and enter the following MicroPython code:

   ```python
   import time

   print("Press `Ctrl+C` to stop")

   try:
       # Forever loop
       while True:
           time.sleep(0.5)

   except KeyboardInterrupt:
       # This part runs when Ctrl+C is pressed
       print("Program stopped. Exiting...")

       # Optional cleanup code
   ```

   This code includes the necessary imports, a forever loop, and the ability to interrupt/stop the program. When you press `Ctrl+C`, it raises a `KeyboardInterrupt` exception on the main thread, stopping the code execution and returning you to the REPL prompt. **We will use this as a template for all future MicroPython applications.**

4. Blinking LED Code: The following code creates an infinite loop where the LED turns on for 0.5 seconds, then off for 0.5 seconds, continuously. The ESP32 controls the onboard LED by sending a HIGH (1) or LOW (0) signal to GPIO Pin 2, which is connected to the LED. The `time.sleep()` function ensures the LED stays on or off for a specific duration.

   ```python
   while True:
       led.on()
       time.sleep(.5)
       led.off()
       time.sleep(.5)
   ```

5. To ensure the LED is turned off when you stop the program, add cleanup code in the exception block:

   ```python
   except KeyboardInterrupt:
       # This part runs when Ctrl+C is pressed
       print("Program stopped. Exiting...")

       # Optional cleanup code
       led.off()
   ```

6. Save the file as `blink.py` in your local folder, and run the code. The onboard LED should start blinking on and off every 0.5 seconds. To stop the execution, press `Ctrl+C` in Thonny's terminal.

<a name="part2"></a>

## Part 2: ESP32 pinout and Breadboard

The ESP32 microcontroller board has a number of **GPIO (General Purpose Input/Output) pins** that can be used for various purposes, such as digital input and output, analog input, communication interfaces (e.g., UART, SPI, I2C), PWM (Pulse Width Modulation) output, and more. The exact pinout may vary depending on the specific development board or module you are using. Here is the pinout for Firebeetle ESP32 board used in the lab:

   ![firebeetle_pinout](images/DFR0478_pinout3.png)

   > **Notes:**
   > * NC = Empty, Not Connected
   > * VCC = VCC (5V under USB power supply, Around 3.7V under 3.7V lipo battery power supply)
   > * Use pins A0, ..., A4 as input only
   > * Do not use In-Package Flash pins

Please note that we will use numerical designations for the GPIO pins in MicroPython. For example, we will refer to the pins as 36, 39, 34, etc., when interacting with the corresponding GPIO numbers located on the right side, starting from the top.

The primary purpose of a **breadboard** (also known as a protoboard or solderless breadboard) is to facilitate the construction and testing of electronic circuits. It allows students to create complex circuits without soldering components together. This is especially important for beginners who are learning electronics and want to experiment with different designs because components can be easily inserted and removed, making it an ideal platform for prototyping and trying out various circuit configurations quickly. Also, breadboards provide a clear visual representation of the circuit layout.

A typical breadboard has rows and columns of interconnected metal clips or sockets, forming a grid. Most breadboards are divided into two halves, usually denoted as the "top" and "bottom" sections. Along the sides of the breadboard, there are usually two long strips, often colored red and blue, which are called the *power rails* used to provide power to your circuits. The red rail is for the positive supply voltage (VCC), and the blue rail is for ground (GND).

The main grid consists of multiple rows and columns. Each row typically contains five interconnected sockets, labeled A, B, C, D, and E. Each column contains interconnected sockets, and columns are often labeled with numbers (1-30, for example). The five sockets within a row are electrically connected. The same goes for sockets within a column; they are electrically connected. The points where the rows and columns intersect are where you can insert and connect components. For example, inserting a wire or component lead into a socket in row "A" and another in column "5" will create an electrical connection between them. For other details see [this](https://computers.tutsplus.com/tutorials/how-to-use-a-breadboard-and-build-a-led-circuit--mac-54746) breadboard description or [that one](https://www.sciencebuddies.org/science-fair-projects/references/how-to-use-a-breadboard).

   ![breadboard](images/breadboard-row-connections.png)

<a name="part3"></a>

## Part 3: LEDs and push buttons

Active-low and active-high are two different methods of connecting and controlling electronic components, such as LEDs (Light Emitting Diodes) and buttons, to an ESP32 GPIO pin. These methods determine the logic levels required to activate (turn on) or deactivate (turn off) the component.

In an **active-low** configuration, the component is activated or considered "on" when the GPIO pin is at a logic LOW (0V or GND) state. When the GPIO pin transitions to a logic HIGH state (3.3V or VCC), the component is turned off.

In an **active-high** configuration, the component is activated when the GPIO pin is at a logic HIGH (3.3V or VCC) state. When the GPIO pin transitions to a logic LOW state (0V or GND), the component is turned off.

### LEDs

For an active-low LED:

* The GPIO pin is connected to the cathode (shorter lead) of the LED.
* The the anode (longer lead) is connected to resistor and 3.3V.
* The LED lights up when the GPIO pin is set to LOW (0).

For an active-high LED:

* The GPIO pin is connected to the anode (longer lead) of the LED.
* The cathode (shorter lead) is connected to resistor and GND.
* The LED lights up when the GPIO pin is set to HIGH (1).

   ![active-low_active-high_led](images/gpio_high_low_easyEda.png)

   ![two-pin-led_pinout](images/LED-polarity.png)

1. Use breadboard, jumper wires and connect at least one LED with a resistor to ESP32 GPIO pins in active-high way. Use GPIO pin number 25 or 26.

   > **IMPORTANT:** On the FireBeetle board, GPIO pins 3 and 1 are dedicated to serial communication with the interactive console via UART. To maintain interactivity, it's advisable to refrain from using these pins for other purposes.

2. Write an application that turns multiple LEDs (including the onboard one) on and off sequentially.

3. Calculating the LED resistor value: Calculate the appropriate resistor value for an LED. The goal is to limit the current flowing through the LED to prevent damage. Use Ohm's Law to calculate the resistance required based on the following:

   * Supply voltage (Vs): 3.3V (Typical for ESP32)
   * LED forward voltage (Vf): 2.0V (Typical for standard red LED)
   * Desired current (I): 20mA (Typical for an LED)

   | **LED Color** | **Typical Forward Voltage (Vf)** |
   |---------------|----------------------------------|
   | Red           | 1.8 - 2.2 V                      |
   | Orange        | 1.9 - 2.2 V                      |
   | Yellow        | 1.9 - 2.2 V                      |
   | Green         | 2.0 - 3.1 V                      |
   | Blue          | 2.8 - 3.7 V                      |
   | White         | 3.0 - 3.5 V                      |

   > **Note:** Note: These are typical values for standard 5mm or SMD LEDs. Actual Vf can vary slightly based on the manufacturer and LED type.

### Buttons

For an active-low button:

* The GPIO pin is connected to one terminal of the button.
* The other terminal is connected to GND.
* The internal (or external) pull-up resistor must be used.
* The button is considered pressed when the GPIO pin reads LOW (0).

For an active-high button:

* The GPIO pin is connected to one terminal of the button.
* The other terminal is connected to VCC (3.3V).
* The internal (or external) pull-down resistor must be used.
* The button is considered pressed when the GPIO pin reads HIGH (1).

   ![active-low_active-high_btn](images/internal_pull-up_arduino.png)

   Note that, the ESP32 has built-in pull-up and pull-down resistors that can be enabled in software.

1. Use breadboard, jumper wires and connect one push button to ESP32 GPIO pin in active-low way. Use GPIO pin number 27.

2. Extend the previous code to keep the onboard LED blinking continuously, while the other LED(s) should blink only when the button is pressed.

   ```python
   ...

   # Define the GPIO pin for the button including internal Pull-up
   btn = Pin(27, Pin.IN, Pin.PULL_UP)

   try:
       # Forever loop
       while True:
           # Check if the button is pressed (active LOW)
           if btn.value() == 0:

               # WRITE YOUR CODE HERE

   ...
   ```

<a name="challenges"></a>

## Challenges

1. Write a MicroPython program that uses all connected LEDs to create a **Knight Rider-style** light pattern whenever a button is pressed. While the button is held down, the LEDs should light up one after another from one end to the other and then reverse direction in a continuous loop. As soon as the button is released, the LEDs should stop and turn off.

2. A **matrix keypad** is a type of input device used to capture user input in the form of numbers, letters, or other characters. It consists of an array of buttons arranged in rows and columns, where each button press represents a unique combination of a row and a column. Matrix keypads are commonly used in various electronic devices, such as calculators and security systems.

Connect the rows and columns of the 4x4 matrix keypad to the GPIO pins of the microcontroller. For example, you might connect the rows (outputs, R1-R4) to GPIO pins 19, 21, 22, 14 (set as `Pin.OUT`), and the columns (inputs, C1-C4) to GPIO pins 12, 4, 16, 17 (set as `Pin.IN, Pin.PULL_UP`).

   ![keypad_pinouts](images/keypad_pinouts.png)

3. Complete the following code, scan the keupad and print the key pressed.

   ```python
   from machine import Pin
   import time

   # Define key layout for a 4x4 keypad
   keys = [
       ['1', '2', '3', 'A'],
       ['4', '5', '6', 'B'],
       ['7', '8', '9', 'C'],
       ['*', '0', '#', 'D']
   ]

   # Define GPIO pins for rows (outputs)
   row_pins = [Pin(pin, Pin.OUT) for pin in (19, 21, 22, 14)]

   # Define GPIO pins for columns (inputs with pull-ups)
   col_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in (12, 4, 16, 17)]


   def scan_keypad():
       for row_num in range(len(row_pins)):
           # Set the current row LOW and the rest HIGH
           # WRITE YOUR CODE HERE

           for col_num in range(len(col_pins)):
               # Read the column input
               # WRITE YOUR CODE HERE


   print("Press a key on the 4x4 keypad (Ctrl+C to exit)")

   try:
       # Forever loop
       while True:
           key = scan_keypad()
           if key:
               print(f"Key pressed: {key}")
               time.sleep(0.01)  # Short debounce delay

   except KeyboardInterrupt:
       # This part runs when Ctrl+C is pressed
       print("Program stopped. Exiting...")

       # Optional cleanup code
   ```

4. Modify the keypad code to control separate LEDs, with each key mapped to an individual LED action.

5. Create a simple, interactive door lock system using a 4x4 keypad, a push button, and two LEDs. The goal is to simulate a password-protected door:

   * The user enters a 4-digit code using the keypad.
   * If any digit is incorrect, the "Access Denied" LED blinks.
   * If the correct password is entered, the "Access Granted" LED lights up, simulating the door unlocking.
   * A physical button acts as the door handle. When the door is unlocked, pressing the button simulates opening the door.

<a name="references"></a>

## References

1. Ben Miller. [How to Use a Breadboard and Build a LED Circuit](https://computers.tutsplus.com/tutorials/how-to-use-a-breadboard-and-build-a-led-circuit--mac-54746)

2. Science buddies. [How to Use a Breadboard for Electronics and Circuits](https://www.sciencebuddies.org/science-fair-projects/references/how-to-use-a-breadboard)

3. Tinker Hobby. [Pull Up Resistors](https://www.tinkerhobby.com/pull-up-resistors/)

4. SparkFun Learn. [Pull-up Resistors](https://learn.sparkfun.com/tutorials/pull-up-resistors/all)

5. Physical Computing. [Lesson 1: Using buttons](https://makeabilitylab.github.io/physcomp/arduino/buttons.html)

6. LEDnique. [LED pinouts - 2, 3, 4-pin and more](https://lednique.com/leds-with-more-than-two-pins/)

7. peppe0. [Use Matrix Keypad with Raspberry PI Pico to get User Codes Input](https://peppe8o.com/use-matrix-keypad-with-raspberry-pi-pico-to-get-user-codes-input/)
