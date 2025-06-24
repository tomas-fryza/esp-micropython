import uasyncio as asyncio
import sys
import os
import time

# Get the starting time in milliseconds
start = time.ticks_ms()


def elapsed():
    """Elapsed time helper."""
    now = time.ticks_ms()
    return time.ticks_diff(now, start)


# Function to generate a unique file name with a three-digit integer
def generate_filename():
    base_name = "output"
    files = os.listdir()

    max_num = 0
    for file in files:
        if file.startswith(base_name) and file.endswith('.txt'):
            try:
                num = int(file[len(base_name):-4])
                max_num = max(max_num, num)  # Find the highest number
            except ValueError:
                continue

    new_file_name = f"{base_name}_{max_num + 1:03d}.txt"
    
    return new_file_name


# Open file for writing (for Process 2)
try:
    fname = generate_filename()
    file = open(fname, 'w')
    print(f"New file `{fname}` created")
except OSError as e:
    print(f"[!] Failed to open file: {e}")
    sys.exit()


# Process 1: Print to serial monitor
async def process_to_serial():
    while True:
        print(f"[{elapsed()}] This is being printed to the serial monitor")
        await asyncio.sleep(1)


# Process 2: Write to file
async def process_to_file():
    while True:
        file.write(f"[{elapsed()}] This is being written to the file\n")
        file.flush()  # Ensure data is written immediately
        await asyncio.sleep_ms(1)


# Main coroutine
async def main():
    print("Starting tasks...")
    task1 = asyncio.create_task(process_to_serial())
    task2 = asyncio.create_task(process_to_file())

    # Run both tasks concurrently
    try:
        await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        print("Tasks cancelled.")


try:
    # Event loop used to schedule and run tasks
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")
    
    # Optional cleanup code
    file.close()
    loop.stop()  # Not available in all uasyncio versions
