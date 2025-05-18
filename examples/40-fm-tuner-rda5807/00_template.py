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
