from machine import Timer, Pin
import machine
import network
import urequests
import json
import neopixel
import time
# import _thread
import wifi_module
import WIFI_CONFIG

# Based on Berman Noam, Bron Matthieu, Clouard Adam
# https://github.com/matthieubron/project-bpa-de2

# Configuration of NeoPixel
pin_neopixel = 5
np = neopixel.NeoPixel(Pin(pin_neopixel), 58)

# GPIO Configuration
btn_w = Pin(27, Pin.IN, Pin.PULL_UP)  # White button
btn_w.irq(trigger = Pin.IRQ_FALLING, handler=lambda pin: handle_debounced(pin, change_color))

led_status = Pin(2, Pin.OUT)
led_status.off()

# Variables Configuration
hour = 0
minute = 0
second = 0

# Different colors for the display
colors = [(255,255,255),(127,0,255),(0,0,255),(0,255,0),(255,0,0)]
color_index = 4
turnoff_color = [(0,0,0)]
turnoff_color_index = 0

# Bounce button
last_press_times = {}

# Creation of the dictionnary for the LED
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
This function sends a request to get the current time
and puts it in the different variables

@return		hours_req		the current hour
@return		minute_req		the courrent minute
@return		second_req		the current seconde
"""
def get_time():
    print("Get time from timeapi.io... ", end="")
    response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague")

    if response.status_code == 200:
        print("Done")
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
        print("Error: ", response.status_code)
        response.close()
        return None, None, None


"""
This function takes care of the incrementation of the time
and uses display_time to show the values on the digital clock

@param _	Identify the pin that triggered the interruption
"""
def update_time(_):
    global hour, minute, second
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
def display_2points(two_points_index, color_index):

    leds = chiffres_leds.get(two_points_index, [])
    for led in leds:
        np[led] = colors[color_index]


"""
This function displays the current time on the digital clock

@param hour			Current hour
@param minute		Current minute
@param color_index	Index that gives the information on which color to chose in the table colors
"""
def display_time(hour, minute, color_index):

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
def turn_off(neopixel_index, number, turnoff_color_index):
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

    debounce_time = 200

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

    print("Button pressed")
    if btn_w.value() == 0:
        if color_index <= len(colors)-2:  # "-2" bcs we're gonna add "1"
            color_index += 1
        else:
            color_index = 0


led_status.on()
wifi_module.connect(wifi, WIFI_CONFIG.SSID, WIFI_CONFIG.PSWD)
for i in range(5):
    hour, minute, second = get_time()
    if hour and minute and second:
        break
wifi_module.disconnect(wifi)
led_status.off()

tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC, callback=update_time)

try:
    while True:
        display_time(hour, minute, color_index)
        time.sleep(0.1)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    led_status.off()
    tim.deinit()  # Stop the timer
    btn_w.irq(trigger=0, handler=update_time)  # Disable the interruption

    turn_off(0,8,0)  # Turn the disaply off
    turn_off(1,8,0)
    turn_off(2,8,0)
    turn_off(3,8,0)
    turn_off_2points(4)
    np.write()
