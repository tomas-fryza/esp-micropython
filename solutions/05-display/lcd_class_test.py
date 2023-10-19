"""
Hardware Configuration:
- Connect the LCD pins to your ESP32 as follows:
  - RS: GPIO pin 1
  - R/W: GND
  - E: 3
  - D7:4: 9, 27, 26, 25

"""

import Lcd
import time

lcd = Lcd(RS=1, E=3, D7=9, D6=27, D5=26, D4=25)

# Forever loop
while True:
    lcd.cursor(1, 3)
    lcd.put_string("Temperature")
    TEMP = 23.25
    TEMP_STR = str(TEMP)
    TEMP_STR = TEMP_STR + chr(223) + "C"
    lcd.cursor(2, 5)
    lcd.put_string(TEMP_STR)

    time.sleep_ms(2000)
    lcd.command(1)
    time.sleep_ms(500)
