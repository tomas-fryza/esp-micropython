from machine import ADC, Pin
from machine import Timer
from hw_config import Button, Led
import time

# Global millisecond counter
cnt = 0


def task_adc():
    """
    Reads and averages both ADCs.
    """
    n_samples = 10
    total1 = 0
    total2 = 0
    for _ in range(n_samples):
        total1 += adc1.read()  # 0--4095 for a 12-bit ADC
        total2 += adc2.read()
        time.sleep_ms(2)  # Slight delay between samples

    # Calculate raw averages
    avg1 = total1 / n_samples
    avg2 = total2 / n_samples

    # Convert to voltage
    volt1 = (avg1 / 4095) * 3.3
    volt2 = (avg2 / 4095) * 3.3

    print(f"X: {avg1} ({volt1:.2f} V)\t Y: {avg2} ({volt2:.2f} V)")


def task_button():
    if btn.is_pressed():
        led.on()
    else:
        led.off()


# Task configuration as a list of dictionaries: each with its
# own period (ms), flag, and function name
tasks = [
    {'period': 250,
     'flag': False,
     'func': task_adc},
    
    {'period': 10,
     'flag': False,
     'func': task_button},
    ]


def timer_handler(t):
    global cnt, tasks
    cnt += 1
    for task in tasks:
        if cnt % task['period'] == 0:
            task['flag'] = True


def run_tasks():
    global tasks
    for task in tasks:
        if task['flag']:
            task['func']()
            task['flag'] = False


# Setup timer interrupt every 1ms
tim = Timer(0)
tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

# Initialize ADC channels
adc1 = ADC(Pin(36))  # Channel X on pin A0 (FireBeetle v2 board)
adc2 = ADC(Pin(39))  # Channel Y on pin A1

# Set ADC attenuation for wider voltage range
adc1.atten(ADC.ATTN_11DB)  # Approx. 0-3.3 V
adc2.atten(ADC.ATTN_11DB)

btn = Button(27)
led = Led(2)

print("ADC started. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        run_tasks()

except KeyboardInterrupt:
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    led.off()
