"""
Battery Voltage Monitor for ESP32 (MicroPython)

This script reads the battery voltage using the ADC on GPIO 34
and prints the value every 5 seconds. It uses a voltage divider 
to scale down the input voltage, and averages multiple ADC 
readings for better accuracy.

Battery + ----[ R1 ]----+----[ R2 ]---- GND
                10k     |      10k
                    ADC Pin (e.g., GPIO 34)

   Vadc = R1 / (R1+R2) * Vbat

Author(s):
- Tomas Fryza

Creation date: 2025-05-26
Last modified: 2025-05-28
"""

from machine import ADC, Pin
import time

VREF = 3.3             # ADC reference voltage
DIVIDER_RATIO = 2.0    # Voltage divider is 1/2
ADC_MAX = 4095.0       # 12-bit ADC


def init_adc(pin_number=34):
    adc = ADC(Pin(pin_number))
    adc.atten(ADC.ATTN_11DB)      # Full-scale voltage ~3.6V
    adc.width(ADC.WIDTH_12BIT)    # 12-bit resolution
    return adc


def read_battery_voltage(adc, samples=10):
    total = 0
    for _ in range(samples):
        total += adc.read()
        time.sleep_ms(10)
    average_raw = total / samples
    voltage = (average_raw / ADC_MAX) * VREF * DIVIDER_RATIO
    return voltage


adc = init_adc()
print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        voltage = read_battery_voltage(adc)
        print(f"Battery voltage: {voltage:.2f} V")
        time.sleep(5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
