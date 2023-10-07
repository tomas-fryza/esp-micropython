def print_arrow(width, symbol):
    """Print an arrow of symbols with a defined width,
       such as `width=5`:
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

    # Print the upper part of the arrow
    for i in range(width):
        arrow_part = symbol * i
        print(arrow_part)

    # Print the lower half of the arrow
    for i in range(width, 0, -1):
        arrow_part = symbol * i
        print(arrow_part)


# Example usage
arrow_width = 5
print_arrow(arrow_width, "*")


def my_factorial(n):
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


# Example usage
n = 1
result = my_factorial(n)
print(f"The factorial of {n} is {result}")


import math   # Import mathematical modul
import cmath  # Complex numbers' math

def solve_quadratic_eq(a, b, c):
    """Solve a quadratic equation of the form ax^2 + bx + c = 0 using
    the quadratic formula:

        x = (-b +- sqrt(b^2 - 4ac)) / (2a)
    """

    # Calculate the discriminant
    disc = b**2 - 4*a*c

    # Check the discriminant for real solutions
    if disc == 0:
        x1 = -b / (2*a)
        x2 = x1  # One real root (repeated)

    elif disc > 0:
        x1 = (-b + math.sqrt(disc)) / (2*a)  # Root square of real value
        x2 = (-b - math.sqrt(disc)) / (2*a)
        # Two distinct real roots

    else:
        # Complex roots (no real solutions)
        x1 = (-b+cmath.sqrt(disc)) / (2*a)  # Root square of complex value
        x2 = (-b-cmath.sqrt(disc)) / (2*a)

    return x1, x2


# Example usage
a = 1
b = 5
c = 1
roots = solve_quadratic_eq(a, b, c)
print(f"Roots: {roots}")
