"""
https://docs.sunfounder.com/projects/esp32-starter-kit/en/latest/micropython/basic_projects/py_joystick.html
https://www.pythontutorials.net/blog/esp32-analog-input-micropython/
https://docs.micropython.org/en/latest/esp32/quickref.html#ADC
"""

from machine import ADC, Pin
from hw_config import Button
from hw_config import Led
import time

# Initialize ADC channels
adc1 = ADC(Pin(36))  # Channel X on pin A0 (FireBeetle v2 board)
adc2 = ADC(Pin(39))  # Channel Y on pin A1

# Set ADC attenuation for wider voltage range
adc1.atten(ADC.ATTN_11DB)  # 150--2450mV range
adc2.atten(ADC.ATTN_11DB)

# Number of samples per reading
NUM_SAMPLES = 5

# Reference voltage (depends on ESP32 supply)
V_REF = 3.3

btn = Button(25)
led = Led(2)


def read_adc_pair(adc1, adc2, samples=NUM_SAMPLES):
    """
    Reads and averages both ADCs, returns raw and voltage values.
    """
    total1 = 0
    total2 = 0
    for _ in range(samples):
        total1 += adc1.read()  # 0--4095 for a 12-bit ADC
        total2 += adc2.read()
        time.sleep_ms(5)  # Slight delay between samples

    # Calculate raw averages
    avg1 = total1 / samples
    avg2 = total2 / samples

    # Convert to voltage
    volt1 = (avg1 / 4095) * V_REF
    volt2 = (avg2 / 4095) * V_REF

    return avg1, volt1, avg2, volt2


try:
    while True:
        raw1, volt1, raw2, volt2 = read_adc_pair(adc1, adc2)
        btnVal = btn.value()

        print(f"X: {raw1:.0f} ({volt1:.2f}V)\t ", end="")
        print(f"Y: {raw2:.0f} ({volt2:.2f}V)\t ", end="")

        if btn.is_pressed():
            print(f"Btn. pressed")
            led.on()
        else:
            print()
            led.off()

        time.sleep(.1)

except KeyboardInterrupt:
    print("Exiting...")
    led.off()
