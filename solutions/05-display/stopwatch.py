"""
Stopwatch on LCD

The example uses Timer and LCD to display a counter in the form of
`minutes:seconds.tenths`. Based of Timer interruptions, the counter
value is updated every 100 milliseconds.

Components:
  - ESP32 microcontroller
  - LCD display:
     + RS: GPIO pin 26
     + R/W: GND
     + E: 25
     + D[7:4]: 27, 9, 10, 13

Author: Tomas Fryza
Creation Date: 2023-10-26
Last Modified: 2024-10-08
"""

from machine import Timer
from lcd_hd44780 import LcdHd44780
import sys


def stopwatch_100ms(t):
    """Interrupt handler of Timer0 executed every 100 millisecs"""
    global tenths  # Can update global variables
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

# Default LCD screen
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

print("Start counting. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        pass

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    lcd.command(0x01)  # Clear display
    timer0.deinit()    # Deinitialize the timer

    # Stop program execution
    sys.exit(0)
