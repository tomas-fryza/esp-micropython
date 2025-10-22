from machine import ADC, Pin
import time

# Initialize ADC channels
adc1 = ADC(Pin(36))  # Channel X on pin A0

# Set ADC attenuation for wider voltage range
adc1.atten(ADC.ATTN_11DB)

print("ADC started. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        val1 = adc1.read()
        print(f"X: {val1}")
        time.sleep(.5)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
