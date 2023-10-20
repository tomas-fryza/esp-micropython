"""
MicroPython mathematical functions

This script defines and demonstrates several mathematical functions.

Instructions:
1. Run the current script
2. Wait for results

Author: Tomas Fryza
Date: 2023-10-12
"""

import math   # Import mathematical module
import cmath  # Complex numbers' math


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
    if width < 3:
        print("Please choose the width greater than or equal to 3.")
        return

    # Print the upper half of the arrow
    for i in range(width):
        arrow_part = symbol * i
        print(arrow_part)

    # Print the lower half of the arrow
    for i in range(width, 0, -1):
        arrow_part = symbol * i
        print(arrow_part)


def my_factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    Args:
        n (int): The integer for which to calculate the factorial.

    Returns:
        int: The factorial of n.

    Example:
        my_factorial(5) returns 120.
    """
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


# Example usage
arrow_width = 5
print_arrow(arrow_width, "*")

n = 7
result = my_factorial(n)
print(f"The factorial of {n} is {result}")

a = 1
b = 5
c = 1
roots = solve_quadratic_eq(a, b, c)
print(f"Roots: {roots}")
