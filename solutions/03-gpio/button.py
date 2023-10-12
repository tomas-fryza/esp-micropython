import machine

# Define the GPIO pin for the button
button_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    button_value = button_pin.value()
    
    # Check if the button is pressed (active LOW)
    if button_value == 0:
        print("Button is pressed")
    else:
        print("Button is released")
