# https://RandomNerdTutorials.com/micropython-esp32-neo-6m-gps/
# https://microcontrollerslab.com/neo-6m-gps-module-esp32-micropython/

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

TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""
GPSdate = ""


def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime, GPSdate

    timeout = time.time() + 8

    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
#         print(parts, len(parts))

        # b'$GPGGA,185406.000,4911.7140,N,01646.2131,E,2,06,1.76,263.0,M,43.4,M,,*\n'
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print()
                print(buff)

                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:]
                GPSdate = ""
                FIX_STATUS = True
                break

        # b'$GPRMC,185420.000,A,4911.7142,N,01646.2135,E,0.36,228.26,180225,,,D*69\r\n'
        if (parts[0] == "b'$GPRMC" and len(parts) == 13):
            if(parts[1] and parts[3] and parts[4] and parts[5] and parts[6] and parts[9]):
#                 print()
#                 print(buff)

                latitude = convertToDegree(parts[3])
                if (parts[4] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[5])
                if (parts[6] == 'W'):
                    longitude = -longitude

                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:]
                GPSdate = parts[9][0:2] + "." + parts[9][2:4] + ".20" + parts[9][4:]

                FIX_STATUS = True
                break

        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)


def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 

    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)


print("\r\nPress `Ctrl+C` to stop")
print("date;time_utc;latitude;longitude")

try:
    while True:
        getGPS(gpsModule)

        if(FIX_STATUS == True):
            print(f"{GPSdate};{GPStime};{latitude};{longitude}")
#             print(f"Date      : {GPSdate}")
#             print(f"Time (UTC): {GPStime}")
#             print(f"Latitude  : {latitude}")
#             print(f"Longitude : {longitude}")
            # print("Satellites: " +satellites)

            FIX_STATUS = False

        if(TIMEOUT == True):
            # print("No GPS data is found.")
            TIMEOUT = False

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
