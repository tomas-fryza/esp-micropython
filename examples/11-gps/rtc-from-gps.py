from machine import Pin, UART, RTC
import time

# Initialize RTC (ESP32 internal RTC)
rtc = RTC()
uart = UART(2, baudrate=9600)  # tx=17 (D10), rx=16 (D11)
led = Pin(2, Pin.OUT)

# Helper function to parse GPS NMEA sentences (basic for GPRMC)
def parse_gprmc(parts):
    if parts[2] == 'A':  # Check if fix is valid
        # Extract UTC time (hhmmss.sss) and date (ddmmyy)
        time_str = parts[1]
        date_str = parts[9]
        hours = int(time_str[0:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        year = 2000 + int(date_str[4:6])
        month = int(date_str[2:4])
        day = int(date_str[0:2])
        
        # Return parsed date and time as a tuple
        return (year, month, day, hours, minutes, seconds)
    return None

# Function to read GPS and update RTC
def update_rtc_from_gps():
    while True:
        # Read data from GPS
        gps_data = str(uart.readline())
        data = gps_data.split(',')

        if (data[0] == "b'$GPRMC" and len(data) == 13):
            if (data[1] and data[2] and data[9]):
                # Parse the GPS data
                gps_time = parse_gprmc(data)
                if gps_time:
                    # Set RTC using GPS time (UTC)
                    rtc.datetime((gps_time[0], gps_time[1], gps_time[2], 0, gps_time[3], gps_time[4], gps_time[5], 0))
                    print(f" Done")
                    return

        print(".", end="")
        time.sleep(1)

# Main function
def main():
    (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
    print(f"Current RTC: {year}-{month}-{day} {hrs}:{mins}:{secs}.{subsecs}")

    print("Waiting for GPS signal (NMEA GPRMC sentence)...", end="")
    led.on()
    update_rtc_from_gps()
    led.off()

    print("\nStart using RTC. Press `Ctrl+C` to stop\n")

    try:
        # Forever loop
        while True:
            (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
            print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}.{subsecs}")
            time.sleep(1)

    except KeyboardInterrupt:
        # This part runs when Ctrl+C is pressed
        print("\nProgram stopped. Exiting...")

        # Optional cleanup code
        led.off()

# Run the main function
main()
