from machine import Pin, Timer, I2C
from neopixel import NeoPixel
import time
import config
import random


LED_PIN = 2
BUTTON_PIN = 27
NEOPIXEL_PIN = 17
NEOPIXEL_NUM = 58
DHT_ADDR = 0x5c

LONG_PRESS_MSEC = 3000

led = Pin(LED_PIN, Pin.OUT)
btn = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
strip = NeoPixel(Pin(NEOPIXEL_PIN, Pin.OUT), NEOPIXEL_NUM)

DIGITS = [
    range(0, 14),     # D0 - hour tens
    range(14, 28),    # D1 - hour ones
    range(30, 44),    # D2 - minute tens
    range(44, 58),    # D3 - minute ones
]

COLON = [28, 29]
COLON_BOTH  = 0
COLON_UPPER = 1
COLON_LOWER = 2
COLON_NONE  = 3

#      2  3
#   1        4
#   0        5
#     12 13
#  11        6
#  10        7
#      9  8

FONT = {
    0: (2,3, 4,5, 6,7, 9,8, 11,10, 1,0),
    1: (4,5, 6,7),
    2: (2,3, 4,5, 12,13, 11,10, 9,8),
    3: (2,3, 4,5, 6,7, 9,8, 12,13),
    4: (1,0, 12,13, 4,5, 6,7),
    5: (2,3, 1,0, 12,13, 6,7, 9,8),
    6: (2,3, 1,0, 12,13, 11,10, 6,7, 9,8),
    7: (2,3, 4,5, 6,7),
    8: (2,3, 4,5, 6,7, 9,8, 11,10, 1,0, 12,13),
    9: (2,3, 1,0, 4,5, 12,13, 6,7, 9,8),
}
DEGREE_SYMBOL = (2,3, 4,5, 12,13, 1,0)
LETTER_C = (2,3, 1,0, 11,10, 9,8)
LETTER_F = (2,3, 1,0, 12,13, 11,10)

colors = [
    (255,   0,   0),   # Red
    (255, 255,   0),   # Yellow
    (128, 255,   0),   # Lime
    (0,   255,   0),   # Green
    (0,   255, 255),   # Cyan
    (0,   128, 255),   # Sky Blue
    (0,     0, 255),   # Blue
    (75,    0, 130),   # Indigo
    (255,  20, 147),   # Pink
    (255, 255, 255),   # White
    (64,   64,  64),   # Dim White
    (32,   32,  32),   # Dimer White
    (8,     8,   8),   # Dimest White
    (0,     0,   0),   # Off
]
color_index = random.randrange(len(colors)-1)
print(f"[neopixel] change color to {colors[color_index]}")

tick_ms = 0
year, month, day, hour, minute, second = 0, 0, 0, 0, 0, 0
temp_c = None
temp_f = None
display_mode = 0  # 0=date, 1=time, 2=temperature_c, 3=temperature_f


def draw_digit(strip, digit_index, value, color):
    base = DIGITS[digit_index]
    segments_on = FONT.get(value, ())

    for i, led in enumerate(base):
        if i in segments_on:
            strip[led] = color
        else:
            strip[led] = (0, 0, 0)


def draw_4digits(strip, left, right, color, colon_mode=COLON_BOTH):
    l_tens = left // 10
    l_ones = left % 10
    r_tens = right // 10
    r_ones = right % 10

    draw_digit(strip, 0, l_tens, color)
    draw_digit(strip, 1, l_ones, color)
    draw_digit(strip, 2, r_tens, color)
    draw_digit(strip, 3, r_ones, color)

    # --- colon handling ---
    if colon_mode == COLON_BOTH:
        strip[COLON[0]] = color
        strip[COLON[1]] = color

    elif colon_mode == COLON_LOWER:
        strip[COLON[0]] = color
        strip[COLON[1]] = (0, 0, 0)

    elif colon_mode == COLON_UPPER:
        strip[COLON[0]] = (0, 0, 0)
        strip[COLON[1]] = color

    else:  # COLON_NONE
        strip[COLON[0]] = (0, 0, 0)
        strip[COLON[1]] = (0, 0, 0)


def draw_symbol(strip, digit_index, segments, color):
    base = DIGITS[digit_index]

    for i, led in enumerate(base):
        strip[led] = color if i in segments else (0, 0, 0)


def is_europe_dst(tm):
    """
    Determine if European Daylight Saving Time (CEST) is in effect.

    Standard time (CET, UTC+1): from last Sunday of October to last Sunday of March
    Daylight saving (CEST, UTC+2): from last Sunday of March to last Sunday of October
    """

    year = tm[0]
    month = tm[1]
    day = tm[2]
    weekday = tm[6]  # 0=Mon ... 6=Sun

    # DST starts: last Sunday of March
    if month < 3 or month > 10:
        return False
    if month > 3 and month < 10:
        return True

    # Compute last Sunday of March / October
    if month == 3:  # March
        last_sunday = 31 - (time.mktime((year, 3, 31, 0, 0, 0, 0, 0)) // 86400 + 3) % 7
        return day >= last_sunday
    elif month == 10:  # October
        last_sunday = 31 - (time.mktime((year, 10, 31, 0, 0, 0, 0, 0)) // 86400 + 3) % 7
        return day < last_sunday
    return False


def sync_rtc(ssid, password, timezone=1):
    import network, ntptime
    from machine import RTC
    import wifi_utils
    import time

    led.on()

    wifi = network.WLAN(network.STA_IF)
    wifi_utils.connect(wifi, ssid, password)

    try:
        ntptime.settime()  # UTC
        now = time.time()
        print(f"[rtc] Get UTC: {now}")

    except OSError as e:
        print("[E] Failed to set RTC:", e)
        led.off()
        return False

    finally:
        wifi_utils.disconnect(wifi)

    # Determine DST
    t_utc = time.localtime(now)
    if is_europe_dst(t_utc):
        tz_sec = (timezone + 1) * 3600  # DST adds +1 hour
        print(f"[rtc] European Daylight Saving Time (CEST) is in effect")
    else:
        tz_sec = timezone * 3600

    # Apply timezone
    t = time.localtime(now + tz_sec)

    rtc = RTC()
    rtc.datetime((
        t[0],  # year
        t[1],  # month
        t[2],  # day
        t[6],  # weekday
        t[3],  # hour
        t[4],  # minute
        t[5],  # second
        0
    ))

    print(f"[rtc] Timezone applied: {t}")
    led.off()

    return True


def task_handle_button():
    """Check button state and call the correct function."""
    global press_start, long_handled

    if not btn.value():  # Pressed (LOW)
        if press_start is None:
            press_start = time.ticks_ms()
            long_handled = False
        else:
            if (not long_handled and
                time.ticks_diff(time.ticks_ms(), press_start) >= LONG_PRESS_MSEC):
                long_press_fn()
                long_handled = True
    else:  # Released
        if press_start is not None and not long_handled:
            short_press_fn()
        press_start = None
        long_handled = False


def short_press_fn():
    global color_index, display_mode
    
    color_index = (color_index + 1) % len(colors)
    print(f"[neopixel] change color to {colors[color_index]}")

    # display_mode = 0
    task_refresh_display()


def long_press_fn():
    sync_rtc(config.SSID, config.PSWD)


def task_read_rtc():
    global year, month, day, hour, minute, second

    t = time.localtime()
    year, month, day, hour, minute, second, _, _ = t


def task_switch_mode():
    global display_mode

    display_mode = (display_mode + 1) % 4
    task_refresh_display()


def task_refresh_display():
    if display_mode == 0:
        # --- Time ---
        print(f"{hour:02d}:{minute:02d}:{second:02d}")
        draw_4digits(strip, hour, minute, colors[color_index], COLON_BOTH)
        strip.write()

    elif display_mode == 1:
        # --- Date ---
        print(f"{year:04d}-{month:02d}-{day:02d}")
        draw_4digits(strip, day, month, colors[color_index], COLON_LOWER)
        strip.write()

    elif display_mode == 2:
        # --- Temperature deg C
        print(f"{temp_c} degC")

        draw_4digits(strip, temp_c, 0, colors[color_index], COLON_NONE)
        draw_symbol(strip, 2, DEGREE_SYMBOL, colors[color_index])
        draw_symbol(strip, 3, LETTER_C, colors[color_index])
        strip.write()

    elif display_mode == 3:
        # --- Temperature deg F
        print(f"{temp_f} degF")

        draw_4digits(strip, temp_f, 0, colors[color_index], COLON_NONE)
        draw_symbol(strip, 2, DEGREE_SYMBOL, colors[color_index])
        draw_symbol(strip, 3, LETTER_F, colors[color_index])
        strip.write()


def task_read_temperature():
    global temp_c, temp_f

    # Read 4 bytes from DHT12 sensor
    # 0x00: humid int
    # 0x01: humid dec
    # 0x02: temp int
    # 0x03: temp dec
    # 0x04: checksum
    a = i2c.readfrom_mem(DHT_ADDR, 0, 4)
    temp = a[2] + a[3]*0.1
    temp_c = round(temp)
    temp_f = int(temp * 9 / 5 + 32 + 0.5)

    print(f"[dht12] temperature: {temp} degC, {temp_f} degF, humid: {a[0]}.{a[1]} %")
    print(temp_c)
    print(temp_f)


# --- Define all periodic tasks in one table ---
tasks = [
    {"func": task_handle_button, "period_ms": 100, "flag": False},
    {"func": task_read_rtc, "period_ms": 1_000, "flag": False},
    {"func": task_switch_mode, "period_ms": 10_000,  "flag": False},
    {"func": task_read_temperature, "period_ms": 60_000,  "flag": False},
]


def timer_handler(t):
    """Interrupt handler for Timer sets task flags."""
    global tick_ms
    tick_ms += 1

    for task in tasks:
        if tick_ms % task["period_ms"] == 0:
            task["flag"] = True


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
display_mode = 0  # Time

sync_rtc(config.SSID, config.PSWD)
task_read_rtc()
task_read_temperature()
task_refresh_display()

# --- State for button handling ---
press_start = None
long_handled = False

# --- Base tick for the whole system ---
Timer(0).init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

# --- Main loop ---
try:
    while True:
        for task in tasks:
            if task["flag"]:
                task["func"]()
                task["flag"] = False

except KeyboardInterrupt:
    print("Program stopped. Exiting...")
    led.off()
    draw_4digits(strip, hour, minute, colors[-1], COLON_NONE)  # Off
    strip.write()
