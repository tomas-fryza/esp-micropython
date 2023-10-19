from machine import Pin

class MyDevice:
    def __init__(self, pin_number):
        # Create a machine.Pin object within the constructor
        self.pin = Pin(pin_number, Pin.OUT)


    def toggle(self):
        self.pin.value(not self.pin.value())


my_device = MyDevice(2)  # Example GPIO pin number (change as needed)
my_device.toggle()  # Toggles the pin state
