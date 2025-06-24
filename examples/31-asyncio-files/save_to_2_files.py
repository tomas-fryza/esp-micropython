# MicroPython builtin modules
import uasyncio as asyncio
import sys
import os
import time


def elapsed():
    """Elapsed time helper."""
    now = time.ticks_ms()
    return time.ticks_diff(now, start)


def generate_filename(prefix):
    """
    Generate a unique file name with a three-digit integer.
    """
    files = os.listdir()

    max_num = 0
    for file in files:
        if file.startswith(prefix) and file.endswith('.txt'):
            try:
                num = int(file[len(prefix):-4])
                max_num = max(max_num, num)  # Find the highest number
            except ValueError:
                continue

    return f"{prefix}_{max_num + 1:03d}.txt"


async def process_to_file1():
    """Task 1"""
    fname = generate_filename("proc1")
    try:
        with open(fname, 'w') as f:
            print(f"New file `{fname}` created")
            while True:
                f.write(f"[{elapsed()}] Task 1\n")
                f.flush()  # Ensure data is written immediately
                await asyncio.sleep_ms(1)
    except OSError as e:
        print(f"[!] File operation failed: {e}")
        sys.exit()


async def process_to_file2():
    """Task 2"""
    try:
        fname = generate_filename("proc2")
        file = open(fname, 'w')
        print(f"New file `{fname}` created")
    except OSError as e:
        print("[!] Failed to open file:", e)
        sys.exit()

    while True:
        file.write(f"[{elapsed()}] Task 2\n")
        file.flush()  # Ensure data is written immediately
        await asyncio.sleep(1)


async def main():
    print("Starting tasks...")
    print("Press `Ctrl+C` to stop")
    task1 = asyncio.create_task(process_to_file1())
    task2 = asyncio.create_task(process_to_file2())

    # Run both tasks concurrently
    try:
        await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        print("Tasks cancelled.")


# Only run if executed directly
if __name__ == "__main__":
    try:
        # Get the starting time in milliseconds
        start = time.ticks_ms()

        # Event loop used to schedule and run tasks
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        # This part runs when Ctrl+C is pressed
        print("Program stopped. Exiting...")
        # Optional cleanup code
        try:
            file.close()
        except NameError:
            pass  # file not defined
        try:
            loop.stop()
        except AttributeError:
            pass  # stop() might not be available
