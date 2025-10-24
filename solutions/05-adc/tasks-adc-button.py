from machine import ADC, Pin
from machine import Timer
from hw_config import Button, Led
import time

tick_ms = 0

led = Led(2)
btn = Button(25)
adc1 = ADC(Pin(36))  # Channel X on pin A0 (FireBeetle v2 board)
adc2 = ADC(Pin(39))  # Channel Y on pin A1
adc1.atten(ADC.ATTN_11DB)  # Approx. 0-3.3 V
adc2.atten(ADC.ATTN_11DB)


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


def task_btn():
    if btn.is_pressed():
        led.on()
    else:
        led.off()


# Define all periodic tasks in one table
tasks = [
    {"func": task_adc, "period": 250, "flag": False},
    {"func": task_btn, "period": 10,  "flag": False},
]


def timer_handler(t):
    """Interrupt handler for Timer runs every 1ms, sets task flags."""
    global tick_ms
    tick_ms += 1

    for task in tasks:
        if tick_ms % task["period"] == 0:
            task["flag"] = True


# 1 ms base tick for the whole system
Timer(0).init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

print("ADC started. Press `Ctrl+C` to stop")
try:
    # Forever loop
    while True:
        for task in tasks:
            if task["flag"]:
                task["func"]()
                task["flag"] = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led.off()
