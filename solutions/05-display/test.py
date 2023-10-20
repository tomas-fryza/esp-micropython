from machine import Pin

class MyDevice:
    def __init__(self, pinrs, pine, pind):
        # Create a list of machine.Pin objects within the constructor
        self.pin_rs = Pin(pinrs, Pin.OUT)
        self.pin_e = Pin(pine, Pin.OUT)
        self.pin_d = [Pin(pin_number, Pin.OUT) for pin_number in pind]

    def toggle(self, pin_index):
        if 0 <= pin_index < len(self.pin_d):
            self.pin_d[pin_index].value(not self.pin_d[pin_index].value())
        else:
            print("Invalid pin_index")
        # print(self.pin_rs)
        # print(self.pin_e)
        # print(self.pin_d)


# Example usage
pinrs = 2
pine = 3  # Replace with your GPIO pin numbers
pind = [25, 26]  # Replace with your GPIO pin numbers
my_device = MyDevice(pinrs, pine, pind)

# Toggle the state of the first pin
my_device.toggle(0)
