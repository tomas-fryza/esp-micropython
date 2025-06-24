# This example makes two LEDs blink at different intervals,
# showcasing how `asyncio` can handle multiple tasks
# concurrently without blocking the execution of other task(s).
#
# See also:
#   https://docs.micropython.org/en/latest/library/asyncio.html
#   https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-2.html
#   https://gpiocc.github.io/learn/micropython/esp/2020/06/13/martin-ku-asynchronous-programming-with-uasyncio-in-micropython.html
#   https://randomnerdtutorials.com/micropython-esp32-esp8266-asynchronous-programming/

from machine import Pin
import time
import uasyncio as asyncio

# Get the starting time in milliseconds
start = time.ticks_ms()

# Setup LED pins
red_led = Pin(7, Pin.OUT)
green_led = Pin(5, Pin.OUT)

# Elapsed time helper
def elapsed():
    now = time.ticks_ms()
    return time.ticks_diff(now, start)

# Define coroutine functions
async def blink_red_led():
    while True:
        print(f"[{elapsed()}] Red toggling")
        red_led.value(not red_led.value())

        # Non-blocking async sleep
        # Pauses only the current coroutine for 0.5 seconds and
        # keeps other tasks running during this time
        await asyncio.sleep(.5)

async def blink_green_led():    
    while True:
        print(f"[{elapsed()}] Green toggling")
        green_led.value(not green_led.value())
        await asyncio.sleep(2)

async def main():
    # Log elapsed time
    print(f"[{elapsed()}] Starting tasks...")

    # Create tasks for blinking two LEDs concurrently
    task1 = asyncio.create_task(blink_red_led())
    task2 = asyncio.create_task(blink_green_led())

    # Run async tasks concurrently, wait for all of them to complete,
    # and keep main() alive while tasks run
    await asyncio.gather(task1, task2)

try:
    # Gets the async "scheduler", the "brain" that controls
    # and runs asynchronous code
    loop = asyncio.get_event_loop()

    # Runs that coroutine until it's completely done
    loop.run_until_complete(main())

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")
    
    # Optional cleanup code
    red_led.off()
    green_led.off()

    loop.stop()  # Not available in all uasyncio versions
