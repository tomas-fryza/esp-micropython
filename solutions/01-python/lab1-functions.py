def print_arrow(width):

    # Print the upper half of the arrow
    for i in range(width):
        arrow_part = "#" * (i+1)
        print(arrow_part)


print_arrow(4)
print_arrow(3)


def factorial(n):
    if n < 0:
        print("No factorial for negative!")
        return
    elif n == 0 or n == 1:
        return 1
    else:
        # WRITE YOUR CODE HERE
        result = 1
        while n > 1:
            result = result * n
            n = n - 1

    return result


print(factorial(-3))
print(factorial(0))
print(factorial(1))
print(factorial(10))


import time

values = range(0, 100)
for i in values:
    print(f"Complete: {i}%", end="\r")
    time.sleep(.05)  # 50 milliseconds delay
print("Complete: 100%")


print("This is \x1b[1;32mGreen and Bold\x1b[0m")
print("\x1b[1;31m[ERROR]\x1b[0m End of file")
