"""
Usage of MicroPython functions

Author: Tomas Fryza
Creation Date: 2023-10-12
Last Modified: 2024-09-20
"""

import time

values = range(0, 100)
for i in values:
    print(f"{i}%", end="\r")
    time.sleep(.05)  # Wait for 50 milliseconds
print("\nProcess complete!")

symbols = ["/", "-", "\\", "|"]
for i in range(10):
    for symbol in symbols:
        print(f"Processing... {symbol}", end="\r")
        time.sleep(.05)
print("Processing... Done")


# Returns the factorial of a given non-negative integer n
def factorial(n):
    if n < 0:
        print("Factorial is not defined for negative numbers")
        return
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        while n > 1:
            result = result * n
            n = n - 1
        return result

n = 7
result = factorial(7)
print(f"The factorial of {n} is {result}")


# Prints the triangle of asterics `*`
def triangle(lines):
    for i in range(lines):
        print("#" * (i+1))

triangle(5)


import math   # Import mathematical module
import cmath  # Complex numbers' math


def solve_quadratic(a, b, c):
    # Calculate the discriminant
    discr = b**2 - 4*a*c

    # Check the discriminant for real solutions
    if discr == 0:
        x1 = -b / (2*a)
        x2 = x1  # One real root (repeated)
    elif discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2*a)
        x2 = (-b - math.sqrt(discr)) / (2*a)
        # Two distinct real roots
    else:
        # Complex roots (no real solutions)
        x1 = (-b+cmath.sqrt(discr)) / (2*a)
        x2 = (-b-cmath.sqrt(discr)) / (2*a)

    return x1, x2

a,b,c = 1,5,1
roots = solve_quadratic(a, b, c)
print(f"Roots of {a}x^2 + {b}x + {c} = 0: {roots}")


# NOTE: In Thonny IDE, enable `\r` and ANSI-color
#       support in menu:
#   Tools > Options... > Shell > Terminal emulation (...)
print("This is \x1b[1;32mGreen and Bold\x1b[0m")
print("\x1b[1;31m[ERROR]\x1b[0m End of file")
