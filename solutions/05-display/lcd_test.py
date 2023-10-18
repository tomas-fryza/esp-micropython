import lcd
import time

# Send initialization sequence
lcd.init()

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
