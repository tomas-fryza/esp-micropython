from machine import Timer,Pin,I2C,PWM
import network
import urequests
import json
import machine
import neopixel
import time
import _thread
from CaptorsConfig import DHT12
from sh1106 import SH1106_I2C
from CaptorsConfig import HCSR04



#    @brief     Controls a Digital clock that display time and have many features
#    @details   This file display the current time on Neopixel Leds, it can also change the timezone, set a timer, an alarm, show temperature and humidity and also change the color of the clock.
#    @author    Berman Noam
#    @author    Bron Matthieu
#    @author    Clouard Adam
#    @version   1.0
#    @date      28/11/2024


# Configuration of NeoPixel

Num_PixelsLed = 14
PIN_NeoPixel = 25

np = neopixel.NeoPixel(machine.Pin(PIN_NeoPixel), (Num_PixelsLed * 4) + 2)


# GPIO Configuration

buttonM = Pin(26,Pin.IN,Pin.PULL_UP)#yellow
buttonL = Pin(27,Pin.IN,Pin.PULL_UP)#white
buttonA = Pin(13,Pin.IN,Pin.PULL_UP) #blue
buttonB = Pin(10,Pin.IN,Pin.PULL_UP) #green
buttonC = Pin(5,Pin.IN,Pin.PULL_UP) #red

buzzer= PWM(Pin(23),freq=1000,duty=0)
buzzer.duty(0)

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor = DHT12(i2c)


# Variables Configuration

mode = 0

hour_req = 0
minute_req = 0
second_req = 0

hour = 0
minute =0
second=0

timer_on = False
timer_sec =0
minute_timer = 0
second_timer = 0

alarm_h = 0
alarm_m = 0
alarm_on = False

temp_digits = []
humidity_digits = []
display_mode = 0

#Different colors for the display

colors = [(255,255,255),(127,0,255),(0,0,255),(0,255,0),(255,0,0)]
color_index = 4
turnoff_color = [(0,0,0)]
turnoff_color_index = 0


#Creation of the list for the TimeZone

time_zone_index = 0
time_zone = [-7,+15,-8]

#Bounce button

last_press_times = {}
debounce_time = 200


SSID = "UREL-SC661-V-2.4G"
PASSWORD = "TomFryza"


#Creation of the dictionnary for the LED

chiffres_leds = {
    0: {
        0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        1: [4, 5, 6, 7],
        2: [2, 3, 4, 5, 8, 9, 10, 11, 12, 13],
        3: [2, 3, 4, 5, 6, 7, 8, 9, 12, 13],
        4: [0, 1, 4, 5, 6, 7, 12, 13],
        5: [0, 1, 2, 3, 6, 7, 8, 9, 12, 13],
        6: [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13],
        7: [2, 3, 4, 5, 6, 7],
        8: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        9: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13]
    },
    1: {
        0: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
        1: [18, 19, 20, 21],
        2: [16, 17, 18, 19, 22, 23, 24, 25, 26, 27],
        3: [16, 17, 18, 19, 20, 21, 22, 23, 26, 27],
        4: [14, 15, 18, 19, 20, 21, 26, 27],
        5: [14, 15, 16, 17, 20, 21, 22, 23, 26, 27],
        6: [14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27],
        7: [16, 17, 18, 19, 20, 21],
        8: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        9: [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27]
    },
    2: {
        0: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
        1: [34, 35, 36, 37],
        2: [32, 33, 34, 35, 38, 39, 40, 41, 42, 43],
        3: [32, 33, 34, 35, 36, 37, 38, 39, 42, 43],
        4: [30, 31, 34, 35, 36, 37, 42, 43],
        5: [30, 31, 32, 33, 36, 37, 38, 39, 42, 43],
        6: [30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43],
        7: [32, 33, 34, 35, 36, 37],
        8: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
        9: [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43]
    },
    3: {
        0: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
        1: [48, 49, 50, 51],
        2: [46, 47, 48, 49, 52, 53, 54, 55, 56, 57],
        3: [46, 47, 48, 49, 50, 51, 52, 53, 56, 57],
        4: [44, 45, 48, 49, 50, 51, 56, 57],
        5: [44, 45, 46, 47, 50, 51, 52, 53, 56, 57],
        6: [44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57],
        7: [46, 47, 48, 49, 50, 51],
        8: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57],
        9: [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 57]

    },
    4 : [28,29],
    5 : [30,31,32,33,34,35,42,43],
    6 : [44,45,46,47,52,53,54,55]

}


wifi = network.WLAN(network.STA_IF)

"""
This function sends a request to connect to the wifi using SSID and PASSWORD
"""
def connect_wifi():
    global wifi
    wifi.active(True)
    print("Connexion au Wi-Fi...")
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(1)
    print("Connecté !")


def disconnect():
    global wifi
    if wifi.active():
        wifi.active(False)

    if not wifi.isconnected():
        print("wifi: Deactivated/disconnected")


"""
This function sends a request to get the current time
and puts it in the different variables

@return		hours_req		the current hour
@return		minute_req		the courrent minute
@return		second_req		the current seconde
"""
def get_time():
    print("Effectuer la requête GET")
    response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague")

    if response.status_code == 200:
        result = response.json()


        hour_req = result.get("hour")
        minute_req = result.get("minute")
        second_req = result.get("seconds")
        print("Hour:", hour_req)
        print("Minute:", minute_req)
        print("Second:",second_req)


        response.close()
        return hour_req, minute_req, second_req
    else:
        print("Erreur lors de la requête:", response.status_code)
        response.close()
        return None, None, None

"""
This function takes care of the incrementation of the time
and uses display_time to show the values on the digital clock

@param _	Identify the pin that triggered the interruption
"""
def update_time(_):
    global hour,minute,second
    second +=1
    if second >=60:
        second = 0
        minute +=1
    if minute >=60:
        minute = 0
        hour +=1
    if hour >=24:
        hour = 0

"""
This function is used to set specific number on Leds

@param neopixel_index		Indicates on which neopixel the number should be display
@param number				Refers to the number in the dictionnary that corresponds to a segment of Leds
@param color_index			Index that gives the information on which color to chose in the table colors
"""
def display_number(neopixel_index,number,color_index):

    leds = chiffres_leds[neopixel_index][number]
    for led in leds:
        np[led] = colors[color_index]


"""
This function is used to set the two points on the Led

@param two_points_index		Refers to the index of the two Leds that control the two points on the clock
@param color_index		    Index that gives the information on which color to chose in the table colors
"""
def display_2points(two_points_index,color_index):

    leds = chiffres_leds.get(two_points_index,[])
    for led in leds:
        np[led] = colors[color_index]


"""
This function displays the current time on the digital clock

@param hour			Current hour
@param minute		Current minute
@param color_index	Index that gives the information on which color to chose in the table colors
"""
def display_time(hour,minute,color_index):

    #Reset the clock by putting all led black corresponds to the number 8 on our device

    turn_off(0,8,0)
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)


    display_number(0,hour // 10,color_index)
    display_number(1,hour % 10,color_index)
    display_2points(4,color_index)
    display_number(2,minute // 10,color_index)
    display_number(3,minute % 10,color_index)
    np.write()



"""
This function turns off the Leds on the neopixel

@param neopixel_index		Indicates on which neopixel the number should be display
@param number				Refers to the number in the dictionnary that corresponds to a segment of Leds
@param turnoff_color_index	Index that gives the information on which color to chose in the table turnoff_color
"""
def turn_off(neopixel_index,number,turnoff_color_index):

    leds = chiffres_leds[neopixel_index][number]
    for led in leds:
        np[led] = turnoff_color[turnoff_color_index]

"""
This function turns off the Leds of the two points

@param two_points_index		Refers to the index of the two Leds that control the two points on the clock
"""
def turn_off_2points(two_points_index):

    leds = chiffres_leds[two_points_index]
    for led in leds:
        np[led] = (0,0,0)



"""
This function makes sure that there is no bounce when we press a button

@param pin		correspond to the pin of the button
@param callback	call the associated function
"""
def handle_debounced(pin, callback):
    global last_press_times
    current_time = time.ticks_ms()

    last_time = last_press_times.get(pin, 0)

    if time.ticks_diff(current_time, last_time) > debounce_time:
        last_press_times[pin] = current_time
        callback(pin)



"""
This function is in charge of the color displayed

@param pin	Identify the pin that triggered the interruption
"""
def change_color(pin):
    global color_index, last_press_time

    print("Button pressed!")
    if buttonL.value() == 0:
        if color_index <= len(colors)-2: # "-2" bcs we're gonna add "1"
            color_index += 1
        else:
            color_index = 0


"""
This function changes the timezone of the time display on the clock

@param pin	Identify the pin that triggered the interruption
"""
def convert_timezone(pin):
    global time_zone_index, hour, minute, color_index

    time_zone_index = (time_zone_index+1)%3
    shift = time_zone[time_zone_index]
    hour = (hour + shift) %24
    display_time(hour,minute,color_index)

"""
This function increases the hour of the alarm by 1

@param pin	Identify the pin that triggered the interruption
"""
def increment_alarm_h(pin):
    global alarm_h,alarm_m,color_index
    alarm_h = (alarm_h+1)%24
    display_time(alarm_h,alarm_m,color_index)

"""
This function increases the minute of the alarm by 1

@param pin	Identify the pin that triggered the interruption
"""
def increment_alarm_m(pin):
    global alarm_h,alarm_m,color_index
    alarm_m = (alarm_m+1)%60
    display_time(alarm_h,alarm_m,color_index)

"""
This function sets either on or off the alarm

@param pin	Identify the pin that triggered the interruption
"""
def alarm_on_off(pin):
    global alarm_on, hour,minute
    alarm_on = not alarm_on
    print(alarm_on)

"""
This function triggers the buzzer when the curent time is equals to alarm time 

@param hour		Current hour
@param	minute	Current minute
"""
def alarm(hour, minute):
    global alarm_on
    if hour == alarm_h and minute == alarm_m and alarm_on:
        for i in range(5):
            display_time(hour,minute,color_index)
            buzzer.duty(512)
            time.sleep(1)
            buzzer.duty(0)
            time.sleep(1)
        alarm_on = False

"""
This function increases the minute of the timer

@param pin	Identify the pin that triggered the interruption
"""
def increment_minute(pin):
    global second_timer,minute_timer,color_index
    minute_timer = (minute_timer+1)%60
    display_time(minute_timer,second_timer,color_index)

"""
This function increases the second of the timer

@param pin	Identify the pin that triggered the interruption
"""
def increment_second(pin):
    global second_timer,minute_timer,color_index
    second_timer = (second_timer+1)%60
    display_time(minute_timer,second_timer,color_index)


"""
This function decrease the times each secondes
and ring a buzzer when the clock reaches 0
"""
def timer():
    global second_timer,minute_timer,color_index
    buzzer_active = False
    while timer_on:

        if minute_timer > 0 and second_timer > 0:
            time.sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer > 0 and second_timer == 0:
            time.sleep(1)
            minute_timer -=1
            second_timer = (second_timer-1)%60
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer > 0:
            time.sleep(1)
            second_timer -=1
            display_time(minute_timer,second_timer,color_index)

        elif minute_timer == 0 and second_timer == 0:
            if not buzzer_active:
                display_time(minute_timer,second_timer,color_index)
                buzzer.duty(512)
                time.sleep(2)
                buzzer.duty(0)
                buzzer_active = True
            time.sleep(1)

"""
This function allows the user to pause or resume the timer

@param pin	Identify the pin that triggered the interruption
"""
def toggle_timer(pin):
    global timer_on

    if timer_on:
        timer_on = False
        print("Timer paused")
    else:
        timer_on = True
        _thread.start_new_thread(timer,())


"""
This function uses the DHT12 sensor to get the current temperature and humidity
"""
def getTemperatureAndHumidity():

    global temp_digits
    global humidity_digits

    temp_digits = []
    humidity_digits = []

    temperature, humidity = sensor.read_values()

    humidity_str = f"{humidity:.2f}"
    temp_str = f"{temperature:.2f}"

    for d in temp_str:
        if d.isdigit():
            temp_digits.append(int(d))

    for d in humidity_str:
        if d.isdigit():
            humidity_digits.append(int(d))

"""
This function allows the user to switch between the temperature mode
and the humidity mode and call a function to display it on the clock

@param pin	Identify the pin that triggered the interruption
"""
def display_change(pin):

    global display_mode
    print(display_mode)

    turn_off(0,8,0)
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)

    if  display_mode == 0:
        display_change_temp()
    else:
        display_change_humidity()

"""
This function display the temperature on the display
and changes the mode to humidity for the next triggered
"""
def display_change_temp():
    global display_mode
    getTemperatureAndHumidity()
    display_number(0,temp_digits[0],color_index)
    display_number(1,temp_digits[1],color_index)
    display_2points(4,color_index)
    display_2points(5,color_index)
    display_2points(6,color_index)
    display_mode = 1
    np.write()
    time.sleep(1)
    return


"""
This function display the humidity on the display
and changes the mode to temperature for the next triggered
"""
def display_change_humidity():
    global display_mode
    getTemperatureAndHumidity()
    print(humidity_digits)
    display_number(0,humidity_digits[0],color_index)
    display_number(1,humidity_digits[1],color_index)
    display_2points(4,color_index)
    display_number(2,humidity_digits[2],color_index)
    display_number(3,humidity_digits[3],color_index)
    display_mode = 0
    np.write()
    time.sleep(1)
    return


"""
This function configures the button depending on the current mode the user is,
so that a button can be configure for different function depending on the mode
"""
def configure_buttons():
    global mode
    buttonA.irq(handler=None)
    buttonB.irq(handler=None)
    buttonC.irq(handler=None)

    if mode == 0:
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, convert_timezone))

    elif mode == 1:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, alarm_on_off))
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_alarm_h))
        buttonC.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_alarm_m))

    elif mode == 2:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, toggle_timer))
        buttonB.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_minute))
        buttonC.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, increment_second))

    elif mode == 3:
        buttonA.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, display_change))



"""
This function takes care of which mode is currently used
and call a function that configure the button depending on the mode

@param pin	Identify the pin that triggered the interruption
"""
def statemode(pin):
    global mode
    mode = (mode + 1)%4
    print(mode)
    configure_buttons()

"""
This function initiates what the clock doesat the beginning of each mode
of the clock
"""
def state():
    if (mode == 0):
        display_time(hour,minute,color_index)

    elif (mode == 1):
        display_time(alarm_h, alarm_m, color_index)

    elif (mode == 2):
        display_time(minute_timer, second_timer, color_index)

    elif (mode == 3):

        pass

"""
This function is the main, sendind the request and therefore
updating the time every 1000ms, while setting the state modes of the clock
"""
#def main():

#    global hour,minute,second,mode
connect_wifi()
hour_req,minute_req,second_req = get_time()
disconnect()
hour =  hour_req
minute =   minute_req
second =  second_req

buttonL.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, change_color))
buttonM.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, statemode))

timer = Timer(0)
timer.init(period = 1000, mode = Timer.PERIODIC, callback = update_time)
while True :
    state()
    alarm(hour,minute)
    time.sleep(0.1)
