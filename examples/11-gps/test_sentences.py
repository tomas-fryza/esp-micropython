# https://RandomNerdTutorials.com/micropython-esp32-neo-6m-gps/
# https://microcontrollerslab.com/neo-6m-gps-module-esp32-micropython/

# NMEA sentence information
# https://aprs.gids.nl/nmea/

# GPGGA:
# https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm?tocpath=Commands%20%2526%20Logs%7CLogs%7CGNSS%20Logs%7C_____59
#
# GPRMC:
# https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm?tocpath=Commands%20%2526%20Logs%7CLogs%7CGNSS%20Logs%7C_____69

from machine import Pin, UART
import utime, time

gpsModule = UART(2, baudrate=9600)  # tx=17 (D10), rx=16 (D11)
print(gpsModule)

buff = bytearray(255)

FIX_STATUS = False

utc = ""
date = ""
lat = ""
lon = ""
sats = ""
alt = ""
speed = 0.0
track = ""


def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, utc, date, lat, lon, sats, alt, speed, track

    timeout = time.time() + 8

    while True:
        # gpsModule.readline()
        buff = str(gpsModule.readline())
        data = buff.split(',')

        # if (data[0] != "b'$GPGGA" and
        #     data[0] != "b'$GPRMC" and
        #     data[0] != "b'$GPGSA" and
        #     data[0] != "b'$GPGSV" and
        #     data[0] != "b'$GPGLL" and
        #     data[0] != "b'$GPVTG"):
        #     print(data[0], len(data))
            # print(data)

        # GPGGA (GPS fix data and undulation)
        if (data[0] == "b'$GPGGA" and len(data) == 15):
            if (data[1] and data[2] and data[3] and data[4] and data[5] and data[7] and data[9]):

                utc = data[1][0:2] + ":" + data[1][2:4] + ":" + data[1][4:]

                lat = convertToDegree(data[2])
                lat += data[3]
                lon = convertToDegree(data[4])
                lon += data[5]

                sats = data[7]  # Number of satellites in use
                alt = data[9]  # Antenna altitude above/below mean sea level (in metres)

                FIX_STATUS = True
                break

        # GPRMC (Recommended minimum specific GPS/transit data)
        if (data[0] == "b'$GPRMC" and len(data) == 13):
            if (data[1] and data[3] and data[4] and data[5] and
                data[6] and data[7] and data[8] and data[9]):

                utc = data[1][0:2] + ":" + data[1][2:4] + ":" + data[1][4:]
                date = "20"+data[9][4:] +"-"+ data[9][2:4] +"-"+ data[9][0:2]

                lat = convertToDegree(data[3])
                lat += data[4]
                lon = convertToDegree(data[5])
                lon += data[6]

                speed = float(data[7]) * 1.852  # kilometers per hour = knots × 1.852
                track = data[8]  # Degrees

                FIX_STATUS = True
                break

        # GPGLL (Geographic position)
        if (data[0] == "b'$GPGLL" and len(data) == 8):
            if (data[1] and data[2] and data[3] and data[4] and
                data[5]):

                utc = data[5][0:2] + ":" + data[5][2:4] + ":" + data[5][4:]

                lat = convertToDegree(data[1])
                lat += data[2]
                lon = convertToDegree(data[3])
                lon += data[4]

                FIX_STATUS = True
                break

        # $GPVTG, Track made good and ground speed
        if (data[0] == "b'$GPVTG" and len(data) == 10):
            if (data[1] and data[7]):

                track = data[1]  # Degrees
                speed = float(data[7])  # kilometers per hour

                FIX_STATUS = True
                break

        utime.sleep_ms(500)


def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 

    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)


print("\nPress `Ctrl+C` to stop\n")
print("datetime;latitude;longitude;sats;alt;speed;track")

try:
    while True:
        getGPS(gpsModule)

        if(FIX_STATUS == True):
            print(f"{date} {utc};{lat};{lon};{sats};{alt};{speed:.2f};{track}")
            FIX_STATUS = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
