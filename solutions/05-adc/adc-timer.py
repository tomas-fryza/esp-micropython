from machine import ADC, Pin
from machine import Timer
import time

# Initialize global counter for different task(s)
cnt = 0

# Task period(s) in milliseconds
PERIOD_ADC = 250

# Task run flags (set in interrupt, read in main loop)
task_adc_run = False

# Number of samples per reading
NUM_SAMPLES = 10


def timer_handler(t):
    """Interrupt handler for Timer runs every 1ms, sets task flags."""
    global cnt, task_adc_run
    cnt += 1

    if cnt % PERIOD_ADC == 0:
        task_adc_run = True


def task_adc(adc1):
    val1 = 0
    for _ in range(NUM_SAMPLES):
        val1 += adc1.read()
        time.sleep_ms(5)

    avg1 = val1 / NUM_SAMPLES
    volt1 = (avg1 / 4095) * 3.3

    return avg1, volt1


# Initialize ADC channels
adc1 = ADC(Pin(36))  # Channel X on pin A0
# Set ADC attenuation for wider voltage range
adc1.atten(ADC.ATTN_11DB)  # 150--2450mV range

# Create an object for 64-bit Timer ID 0
tim = Timer(0)

# Start the Timer
tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

print("ADC started. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        if task_adc_run:
            avg1, volt1 = task_adc(adc1)
            print(f"[{cnt}] X: {avg1:.0f} ({volt1:.2f}V)")
            task_adc_run = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
