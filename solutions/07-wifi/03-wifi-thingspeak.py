import network
from machine import I2C
from machine import Pin
import time
import urequests  # Network Request Module

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
THINGSPEAK_API_KEY = "<THINGSPEAK WRITE API KEY>"

# DHT12 I2C address
SENSOR_ADDR = 0x5c

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

# I2C(id, scl, sda, freq)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)


def connect_wifi():
    """
    Connect to Wi-Fi network.

    Activates the Wi-Fi interface, connects to the specified network,
    and waits until the connection is established.

    :return: None
    """
    from time import sleep_ms

    if not wifi.isconnected():
        print(f"Connecting to `{WIFI_SSID}`", end="")

        # Activate the Wi-Fi interface
        wifi.active(True)

        # Connect to the specified Wi-Fi network
        wifi.connect(WIFI_SSID, WIFI_PSWD)

        # Wait untill the connection is estalished
        while not wifi.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")
    else:
        print("Already connected")


def disconnect_wifi():
    """
    Disconnect from Wi-Fi network.

    Deactivates the Wi-Fi interface if active and checks if
    the device is not connected to any Wi-Fi network.

    :return: None
    """
    # Check if the Wi-Fi interface is active
    if wifi.active():
        # Deactivate the Wi-Fi interface
        wifi.active(False)

    # Check if the device is not connected to any Wi-Fi network
    if not wifi.isconnected():
        print("Disconnected")


def read_dht12_sensor():
    val = i2c.readfrom_mem(SENSOR_ADDR, 0, 5)

    # Verify the checksum
    if (val[0] + val[1] + val[2] + val[3]) & 0xff != val[4]:
        raise Exception("DHT12 checksum error")
    
    temp = val[2] + (val[3]*0.1)
    humi = val[0] + (val[1]*0.1)

    return temp, humi


print("Stop the code execution by pressing `Ctrl+C` key.")
print("")
print("Scanning I2C... ", end="")
addrs = i2c.scan()
if SENSOR_ADDR in addrs:
    print(f"{hex(SENSOR_ADDR)} detected")
else:
    raise Exception(f"Sensor `{hex(SENSOR_ADDR)}` is not detected")

try:
    while True:
        temp, humidity = read_dht12_sensor()
        print(f"Temperature: {temp} C\tHumidity: {humidity} %")
        # send_to_thingspeak(temp, humidity)
        time.sleep(60)

        # TODO:
        # def send_to_thingspeak(temp, humidity):
        #     url = f"{api_url}?api_key={api_key}&field1={temp}&field2={humidity}"
        #     response = urequests.get(url)
        #     print("Response:", response.text)
        #     response.close()


        # connect_wifi()
        #
        # Send data using a POST request
        # request = urequests.post(
        #     'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_API_KEY,
        #     json={"field1": temp, "field2": humi},
        #     headers={"Content-Type": "application/json"})
        # print(f"Response: {request.text}")
        # request.close()
        #
        # disconnect_wifi()


except KeyboardInterrupt:
    print("Ctrl+C Pressed. Exiting...")
