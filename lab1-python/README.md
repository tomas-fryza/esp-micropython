# Lab 1: Programming in Python

* [Pre-Lab preparation](#preparation)
* [Part 1: Basic operations in Python](#part2)
* [Part 2: Functions in Python](#part3)
* [Part 3: Control characters and ANSI-color](#part4)
* [Challenges](#challenges)
* [References](#references)

### Components list

* ESP32 board, USB cable

### Learning objectives

* Understand Python's syntax, data types, and basic programming concepts like variables and basic operations.
* Use control structures like loops (`for` and `while`), `if` statements, and `else` clauses to control the flow of your programs.
* Understand the concept of functions, how to define them, pass arguments, and return values.

<a name="preparation"></a>

## Pre-Lab preparation

1. Remind yourself the basic control structures in Python.

<a name="part1"></a>

## Part 1: Basic operations in Python

1. Use micro USB cable and connect the ESP32 board to your computer. Run Thonny IDE and check if selected interpreter is Micropython (ESP32). If not, go to menu **Run > Select interpreter... > Interpreter** and select `ESP32` or `ESP8266`. Click on red **Stop/Restart** button or press the on-board reset button if necesary.

2. In the **Shell** window, attempt the following arithmetic, binary, and string operations using variables. Note that you can use the `print()` function  to display values or text.

    ```python
    # Arithmetic operations
    >>> 10/3
    3.333333
    >>> 10//3
    3
    >>> 10%3
    1
    >>> 10*3
    30
    >>> 10**3
    1000
    ```

    ```python
    # Binary operations
    >>> a = 5  # Binary: 0101
    >>> b = 3  # Binary: 0011
    >>> result = a & b
    >>> print(result)

    >>> result = a | b
    >>> print(f"Bitwise OR result is {result}")

    >>> result = a ^ b
    >>> print(f"Bitwise XOR result is {result}")

    >>> result = ~a
    >>> print(f"Bitwise NOT of {a} is {result}")

    >>> left_shifted = a << 1
    >>> print(f"Left shift {a} is {left_shifted}")
    ```

    ```python
    # String operations
    >>> str1 = "Hello, "
    >>> str2 = "world!"
    >>> text = str1 + str2
    >>> print(text)

    >>> result = str1 * 4
    >>> print(result)

    >>> length = len(result)
    >>> print(length)

    >>> first_char = text[0]
    >>> third_char = text[2]
    >>> last_char = text[-1]
    >>> print(...)
    ```

    ```python
    # Get the current frequency of the CPU and RTC time
    >>> import machine
    >>> help(machine)
    >>> machine.freq()
    >>> machine.RTC().datetime()

    # Get Flash size in Bytes
    >>> import esp
    >>> esp.flash_size()

    # Read the internal temperature (in Fahrenheit)
    >>> import esp32
    >>> esp32.raw_temperature()
    # FYI: temp_c = (temp_f-32) * (5/9)
    #      temp_f = temp_c * (9/5) + 32
    ```

<a name="part2"></a>

## Part 2: Functions in Python

<<<<<<< HEAD
=======
1. In Thonny IDE, create a new source file in menu **File > New Ctrl+N**, save it as `functions.py` to your local folder. Program the function to display an `arrow` of symbols and run the application by **Run > Run current script F5**. Note that you can use **if** statements and **for** loops.

    ```python
    def print_arrow(width, symbol):
        """
        Print an arrow made of symbols with a defined width.

        Args:
            width (int): The width of the arrow.
            symbol (str): The symbol used to create the arrow.

        Example:
            print_arrow(5, "*") would print:
            *
            **
            ***
            ****
            *****
            ****
            ***
            **
            *
        """
        # Complete the code

    # Example usage
    arrow_width = 5
    print_arrow(arrow_width, "*")
    ```

2. Create a function `my_factorial(n)` to calculate a factorial of input `n`.

3. Create a function `def solve_quadratic_eq(n)` to solve the quadratic equation.

    ```python
    def solve_quadratic_eq(a, b, c):
        """
        Solve a quadratic equation of the form ax^2 + bx + c = 0.

        Args:
            a (float): Coefficient of x^2.
            b (float): Coefficient of x.
            c (float): Constant term.

        Returns:
            tuple: A tuple containing the real or complex roots.

        Example:
            solve_quadratic_eq(1, 5, 1) returns the roots (approximately):
            (-0.2087, -4.7912)
        """
        # Complete the code

    # Example usage
    a = 1
    b = 5
    c = 1
    roots = solve_quadratic_eq(a, b, c)
    print(f"Roots: {roots}")
    ```

    If you require a library function in Python, you need to import the module that contains it.

    ```python
    import math  # Import mathematical module
    import cmath  # Complex numbers' math
    
    math.sqrt()  # Call the function
    ```

<a name="part3"></a>

## Part 3: Control characters and ANSI-color

>>>>>>> 0fc769eb19f547d1e95d25b88562e4e2e92cd9b2
In MicroPython, you can use the following control characters and escape sequences to format text, especially when working with the REPL (Read-Eval-Print Loop) and terminal output:

   * **Newline (\n):** Creates a new line, moving the cursor to the beginning of the next line.

   * **Carriage Return (\r):** Moves the cursor to the beginning of the current line. Useful for overwriting text on the same line.

   * **Tab (\t):** Inserts a horizontal tab, which typically advances the cursor to the next tab stop. Tab stops are usually set at regular intervals, such as every 4 or 8 spaces.

   * **Backspace (\b):** Moves the cursor one position to the left. Useful for removing characters.

   * **Escape (\x1b):** Starts an escape sequence that can be used to control text formatting, colors, and other terminal features. For example, you can change text color using ANSI escape codes.

**Important:** To use these characters and sequences in Thonny IDE, enable the support in menu **Tools > Options... > Terminal emulation**.

1. In Thonny IDE, create a new source file in menu **File > New Ctrl+N**, save it as `functions.py` to your local folder. Use the following example using a control character `\r` and create a processing counter. Run the application by **Run > Run current script F5**.

   ```python
   import time

   values = range(0, 100)
   for i in values:
       print(f"Complete: {i}%", end="\r")
       time.sleep(.1)
   ```

2. Write a Python function that calculates the factorial of a given number `n`. The function should take one input parameter, `n`, and return the result of `n!` (`n` factorial), which is the product of all positive integers from 1 to `n`. Note that you can use **if** statements and **while** loops.

   For example:
      * factorial(5) should return 120 because 5! = 5 * 4 * 3 * 2 * 1 = 120.
      * factorial(0) should return 1, as the factorial of 0 is defined to be 1.

   ```python
   def factorial(n):
       # If negative inputs, then Error

       # Elif input is zero or one, then return 1

       # Else other input values, then
       # result = n * (n-1) * (n-2) * ... * 1
   ```

3. Write a Python function that prints a right-angled triangle made up of asterisks (`*`). The function should take one parameter, which specifies the number of lines in the triangle. Each subsequent line should contain one additional asterisk, starting with one asterisk on the first line, two on the second line, and so on. 

   For example, if the parameter is `5`, the output should look like this:

   ```shell
   *
   **
   ***
   ****
   *****
   ```

   ```python
   def triangle(lines):
       # WRITE YOUR CODE HERE

   # Example usage
   triangle(5)
   ```

4. Write a Python function to solve a quadratic equation of the form `ax^2 + bx + c = 0`, where `a`, `b`, and `c` are real numbers. The function should take three input parameters: `a`, `b`, and `c`. Use the quadratic formula to find the solutions:

   \[
   x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
   \]

   Your function should:
      1. Handle cases where the equation has two real solutions.
      2. Handle cases where there is only one real solution (when the discriminant is zero).
      3. Indicate if the equation has no real solutions (when the discriminant is negative).

   For example:
      - For inputs `a = 1`, `b = -3`, and `c = 2`, the function should return two solutions: `x1 = 2` and `x2 = 1`.
      - For inputs `a = 1`, `b = 2`, and `c = 1`, the function should return one solution: `x = -1`.
      - If the discriminant is negative, return a message indicating there are no real solutions.

   ```python
   def solve_quadratic_eq(a, b, c):
       """
       Solve a quadratic equation of the form ax^2 + bx + c = 0.

       Args:
           a (float): Coefficient of x^2.
           b (float): Coefficient of x.
           c (float): Constant term.

       Returns:
           tuple: A tuple containing the real or complex roots.

       Example:
           solve_quadratic_eq(1, 5, 1) returns the roots (approximately):
           (-0.2087, -4.7912)
       """
       # WRITE YOUR CODE HERE

   # Example usage
   a = 1
   b = 5
   c = 1
   roots = solve_quadratic_eq(a, b, c)
   print(f"Roots: {roots}")
   ```

   If you require a library function in Python, you need to import the module that contains it.

   ```python
   import math  # Import mathematical module
   import cmath  # Complex numbers' math
    
   math.sqrt()  # Call the function
   ```

<a name="challenges"></a>

## Challenges

1. Write a Python function that determines whether a given number is prime or not and generate all prime numbers up to 1000.

2. Implement a function to generate Fibonacci numbers. This is a classic sequence where each number is the sum of the two preceding ones (0, 1, 1, 2, 3, 5, 8, ...).

3. See the following example and use different [ANSI Escape Sequences](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797) to modify style and color of the printed text:

   ```python
   print("This is \x1b[1;32mGreen and Bold\x1b[0m")
   print("\x1b[1;31m[ERROR]\x1b[0m End of file")
   ```

<a name="references"></a>

## References

1. [Markdown Guide, Basic Syntax](https://www.markdownguide.org/basic-syntax/)

2. [learnpython.org](https://www.learnpython.org/)

3. Tomas Fryza. [Useful Git commands](https://github.com/tomas-fryza/esp-micropython/wiki/Useful-Git-commands)

4. Joshua Hibbert. [Git Commands](https://github.com/joshnh/Git-Commands)
