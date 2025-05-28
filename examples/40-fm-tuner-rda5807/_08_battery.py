#
# Battery + ----[ R1 ]----+----[ R2 ]---- GND
#                 10k     |      10k
#                     ADC Pin (e.g., GPIO 34)
#
#   Vadc = R1 / (R1+R2) * Vbat
#

from machine import ADC, Pin
import time

# Constants
VREF = 3.3         # ADC reference voltage
DIVIDER_RATIO = 2  # Voltage divider is 1/2
ADC_MAX = 4095     # 12-bit ADC


def read_battery_voltage():
    raw = adc.read()
    voltage = (raw / ADC_MAX) * VREF * DIVIDER_RATIO
    return voltage


adc = ADC(Pin(34))          # Configure ADC (GPIO 34)
adc.atten(ADC.ATTN_11DB)    # Allows full scale voltage ~3.6V
adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        voltage = read_battery_voltage()
        print(f"Battery Voltage: {voltage:.2f} V")
        time.sleep(2)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
