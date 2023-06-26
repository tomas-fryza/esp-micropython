from machine import Timer
from machine import Pin

def toggleLed(t):
    led.value(not led.value())

def mycallback(t):
    global counter
    counter += 1
    print(f"Timer1 interrupted {counter} times")


led = Pin(2, Pin.OUT)
counter = 0

# ESP32 has four 64-bit hardware timers (Timer0, Timer1, Timer2, Timer3)
# based on 16-bit pre-scalers

# Create a timer object
tim0 = Timer(0)
# Periodically invert LED value 10 times per second
tim0.init(mode=Timer.PERIODIC, freq=10, callback=toggleLed)

# Periodically call function every two seconds
tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC, freq=.5, callback=mycallback)

# Print info just ones after 500 millisecs
tim2 = Timer(2)
tim2.init(mode=Timer.ONE_SHOT, period=500, callback=lambda t:print("Timer2 callback"))

# Stop and disable Timer1 peripheral after 10 secs
tim3 = Timer(3)
tim3.init(mode=Timer.ONE_SHOT, period=10000, callback=lambda t:tim1.deinit())
