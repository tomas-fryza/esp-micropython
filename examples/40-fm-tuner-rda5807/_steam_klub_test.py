
# https://101-things.readthedocs.io/en/latest/fm_radio.html
# https://github.com/wagiminator/ATtiny85-TinyFMRadio/blob/master/software/TinyFMRadio.ino
# https://github.com/pu2clr/RDA5807/tree/master/examples
# https://maker.pro/arduino/projects/simple-fm-radio-receiver-with-arduino-uno-and-rda5807m

# https://github.com/franckinux/python-rd5807m/tree/master






# Micropython builtin modules
import time
from machine import Pin, SoftI2C, RTC, PWM
from math import floor
# from dht import DHT11

# External modules
import ssd1306              # OLED
# from bh1750 import BH1750   # Lux meter
from bmp180 import BMP180   # Pressure meter
# from MPU6050 import MPU6050 # Accelerometer + gyroscope
import rda5807              # FM radio module


# DHT11: Data - 4
# Temperature + Humidity
# d = DHT11(Pin(4, Pin.IN, Pin.PULL_UP)) # The input mode and pull-up need to be set manually!

# Piezo buzzer - 13
# buzzer = PWM(Pin(13, Pin.OUT), duty=0) # duty=0 prevents default waveform from starting immediately

# PIR sensor: GPIO 14
pir = Pin(15, Pin.IN)

# Capacitive touch sensor: GPIO 12
# touch = Pin(12, Pin.IN)

# I2C devices: SDA - 21, SCK - 22
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400_000)

# OLED
display = ssd1306.SSD1306_I2C(128, 32, i2c) # using default address 0x3C

# Lux meter
# bh1750 = BH1750(0x23, i2c)

# Pressure meter
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

# Led & buttons
led = Pin(2, Pin.OUT)
led.off()
btn_gr = Pin(19, Pin.IN, Pin.PULL_UP)
btn_rd = Pin(18, Pin.IN, Pin.PULL_UP)
btn_rot = Pin(25, Pin.IN, Pin.PULL_UP)

# Accelero + gyroscope
# mpu = MPU6050(i2c)

# FM Radio module
radio = rda5807.Radio(i2c)
time.sleep_ms(100)  # Let the radio initialize!!! Without the sleep the module does not work!
# init with default settings
radio.set_volume(1) # 0-15
radio.set_frequency_MHz(103.0) # Radio Krokodyl (Brno)
radio.mute(False)

# Piezo buzzer 100ms beep
# buzzer.freq(4095)
# buzzer.duty(50)
# time.sleep(0.1)
# buzzer.duty(0)
# buzzer.deinit()


# Custom function definitions
def floatToStr(f: float):
    return str(round(f, 2)) # Max 2 decimal digits


try:
    # Main loop
    while True:
        if (btn_gr.value() == 0) or (btn_rd.value() == 0) or (btn_rot.value() == 0):
            led.on()
        else:
            led.off()

        display.fill(0)
        
        # Lux + pressure meter + PIR + Capacitive touch
        # display.text(floatToStr(bh1750.measurement)+' lx', 0, 0, 1)
        # display.text(floatToStr(bmp180.pressure/1000)+' kPa', 0, 8, 1)
        # display.text(floatToStr(bmp180.temperature)+' \'C', 0, 16, 1)
        display.text('PIR: '+str(pir.value()), 0, 24, 1)
        # display.text('Touch: '+str(touch.value()), 56, 24, 1)
        
        # Accelerometer
        #accel = mpu.read_accel_data()
        #gyro = mpu.read_gyro_data()
        #temp = mpu.read_temperature()
        #Xstr = 'X % 3d.%02d % 3d.%02d' % (floor(accel["x"]), round(100*(accel["x"]%1)), floor(gyro["x"]), round(100*(gyro["x"]%1)))
        #Ystr = 'Y % 3d.%02d % 3d.%02d' % (floor(accel["y"]), round(100*(accel["y"]%1)), floor(gyro["y"]), round(100*(gyro["y"]%1)))
        #Zstr = 'Z % 3d.%02d % 3d.%02d' % (floor(accel["z"]), round(100*(accel["z"]%1)), floor(gyro["z"]), round(100*(gyro["z"]%1)))
        #display.text(Xstr, 0, 0, 1)
        #display.text(Ystr, 0, 8, 1)
        #display.text(Zstr, 0, 16, 1)
        #display.text('Temp '+floatToStr(temp)+' \'C', 0, 24, 1)
        
        # DHT11: Temperature + Humidity
        #try:
        #    d.measure()
        #    display.text('DHT11', 0, 0, 1)
        #    display.text('Temp: '+str(d.temperature())+' \'C', 0, 10, 1)
        #    display.text('Humi: '+str(d.humidity())+' %', 0, 20, 1)
        #except:
        #    display.text('DHT11 meas. fail', 0, 0, 1)
        
        # FM Radio
        display.text(str(radio.get_frequency_MHz())+' MHz', 0, 0, 1)
        rssi = radio.get_signal_strength()
        print(rssi, "dBm")
        radio.update_rds()
        # print(radio.get_rds_block_group()) # How to decode RDS?
        print(radio.station_name)

        display.show()
        time.sleep_ms(100)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led.off()
