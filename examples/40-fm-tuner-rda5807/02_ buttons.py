from machine import Pin
from machine import PWM
import time


# Interrupt callbacks
def btn_0_isr(pin):
    # Debounce delay
    time.sleep_ms(20)
    if pin.value() == 0:  # Button pressed (active-low)
        led_0.value(not led_0.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_0.value()}")
    
    
def btn_1_isr(pin):
    time.sleep_ms(20)
    if pin.value() == 0:
        led_1.value(not led_1.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_1.value()}")


def btn_2_isr(pin):
    time.sleep_ms(20)
    if pin.value() == 0:
        led_2.value(not led_2.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_2.value()}")


def btn_3_isr(pin):
    time.sleep_ms(20)
    if pin.value() == 0:
        led_3.value(not led_3.value())
        print(f"Btn pressed: {pin}")
        print(f"LED value: {led_3.value()}")


def btn_rot_isr(pin):
    time.sleep_ms(20)
    if pin.value() == 0:
        print(f"Rot. encoder pressed: {pin}")
        beep()


def beep(freq=1500, duration_ms=60, duty_cycle=40):
    buzzer.freq(freq)
    buzzer.duty(duty_cycle)
    time.sleep_ms(duration_ms)
    buzzer.duty(0)


# LEDs
led_builtin = Pin(2, Pin.OUT)
led_builtin.off()
led_0 = Pin(19, Pin.OUT)
led_1 = Pin(18, Pin.OUT)
led_2 = Pin(5, Pin.OUT)	
led_3 = Pin(17, Pin.OUT)

# Buttons
btn_0 = Pin(4, Pin.IN)
btn_1 = Pin(0, Pin.IN)
btn_2 = Pin(2, Pin.IN)
btn_3 = Pin(15, Pin.IN)
btn_rot = Pin(33, Pin.IN)

# Attach buttons' interrupts
btn_0.irq(trigger=Pin.IRQ_FALLING, handler=btn_0_isr)
btn_1.irq(trigger=Pin.IRQ_FALLING, handler=btn_1_isr)
btn_2.irq(trigger=Pin.IRQ_FALLING, handler=btn_2_isr)
btn_3.irq(trigger=Pin.IRQ_FALLING, handler=btn_3_isr)
btn_rot.irq(trigger=Pin.IRQ_FALLING, handler=btn_rot_isr)

# Start buzzer with duty=0 (silent)
buzzer = PWM(Pin(13, Pin.OUT), duty=0)

print("Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_0.off()
    led_1.off()
    led_2.off()
    led_3.off()
    btn_0.irq(handler=None)  # Disables IRQ triggers
    btn_1.irq(handler=None)
    btn_2.irq(handler=None)
    btn_3.irq(handler=None)
    btn_rot.irq(handler=None)
    buzzer.deinit()
