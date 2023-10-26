"""
Stopwatch on LCD

The example uses Timer0 and LCD to display a counter in the form of
`minutes:seconds.tenths`. Based of Timer0 interruptions, the counter
value is updated every 100 milli seconds.

Hardware Configuration:
- Connect HD44780-based LCD to your ESP32 as follows:
  - RS: GPIO pin 26
  - R/W: GND
  - E: 25
  - D7:4: 27, 9, 10, 13

Instructions:
1. Connect the LCD display to GPIO pins
2. Run the script
3. Stop the code execution by pressing `Ctrl+C` key.
   If it does not respond, press the onboard `reset` button.

Author: Tomas Fryza
Date: 2023-10-26
"""

# Import necessary module(s)
from lcd_hd44780 import LcdHd44780
from machine import Timer


def stopwatch_100ms(t):
    """Interrupt handler of Timer0 executed every 100 millisecs"""
    global tenths  # Can use global variable here
    global secs

    # Modify tenths of seconds
    tenths += 1
    if tenths >= 10:
        tenths = 0
        secs += 1
        
        # Modify seconds
        if secs >= 60:
            secs = 0
        # Display seconds
        lcd.move_to(2,6)
        if secs < 10:
            lcd.write("0")
        lcd.write(str(secs))

    # Display tenths of seconds
    lcd.move_to(2, 9)
    lcd.write(str(tenths))


# Initialize LCD (four-data pins order is [D4, D5, D6, D7])
lcd = LcdHd44780(rs=26, e=25, d=[13, 10, 9, 27])

# Default screen
lcd.move_to(1, 1)
lcd.write("Stopwatch:")
lcd.move_to(2, 3)
lcd.write("00:00.0")

# Define 100-millisec timer
timer0 = Timer(0)
timer0.init(period=100,
            mode=Timer.PERIODIC,
            callback=stopwatch_100ms)

tenths = 0  # Global variable for `tenths of seconds`
secs = 0    # ... and for seconds

print("Stop the code execution by pressing `Ctrl+C` key.")
print("If it does not respond, press the onboard `reset` button.")
print("")
print("Start counting...")

# Forever loop until interrupted by Ctrl+C. When Ctrl+C
# is pressed, the code jumps to the KeyboardInterrupt exception
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")

    # Optional cleanup code
    lcd.command(0x01)  # Clear display
    timer0.deinit()    # Deinitialize the timer
