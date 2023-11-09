# Lab 7: Wi-Fi communication

## Wi-Fi scan

The Wi-Fi scanning process on the ESP32 involves searching for available Wi-Fi networks in the vicinity. This is commonly used to provide information about nearby networks or to allow the ESP32 to connect to a specific Wi-Fi network.

![wifi-scan](images/ESP32-WiFi-Scan-Networks_Wi-Fi-Scan.png)

Use the following code to create an instance of the `WLAN` class from the `network` module, specifying the desired Station mode, activate the Wi-Fi interface, and perform Wi-Fi scan.

See the documentation for [WLAN class](https://docs.micropython.org/en/latest/library/network.WLAN.html) description.

```python
import network

# Initialize the Wi-Fi interface in Station mode and activate it
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Perform the Wi-Fi scan
print("Scanning for Wi-Fi... ", end="")
nets = wifi.scan()
print(f"{len(nets)} networks")

# Print the list of available Wi-Fi networks
print("RSSI Channel \tSSID")
for net in nets:
    rssi = net[3]
    channel = net[2]
    ssid = net[0].decode("utf-8")
    print(f"{rssi}  (ch.{channel}) \t{ssid}")
```

> **Note:** The `.decode("utf-8")` method converts a sequence of bytes into a string using the UTF-8 encoding.

## Wi-Fi Station mode

ESP32 microcontrollers typically have two main modes of operation for the Wi-Fi interface: Station mode and Access Point mode.

In **Station Mode (`network.STA_IF`)** the ESP32 connects to an existing Wi-Fi network as a client. It can obtain an IP address from the network and access the Internet. This mode is suitable for scenarios where the ESP32 needs to connect to an existing Wi-Fi network, like a home or office network.

![wifi-sta](images/ESP32-Station-Mode.png)

In **Access Point mode (`network.AP_IF`)** the ESP32 acts as a Wi-Fi access point (AP) and other devices (like smartphones or computers) can connect to the ESP32 and obtain an IP address. This mode is useful when you want the ESP32 to create its own Wi-Fi network.

![wifi-ap](images/ESP32-Access-Point-Mode.png)

The Wi-Fi modes can be activated or deactivated using the `active()` method of the `network` module. These modes can be used individually or in combination. For example, the ESP32 can operate in both Station and Access Point modes simultaneously (`network.WIFI_AP_STA`), allowing it to connect to an existing Wi-Fi network while also providing an access point for other devices.

In MicroPython on the ESP32, the `network.STA_IF` provides access to the interface's configuration and status. Use the following code, set your Wi-Fi settings, and connect to the network.

```python
import network

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"

# Initialize the Wi-Fi interface in Station mode
wifi = network.WLAN(network.STA_IF)


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


connect_wifi()

# WRITE YOUR CODE HERE

disconnect_wifi()
```

When working with the `network.WLAN` class, `ifconfig()` is used to get or set the IP configuration of the interface. Place the following codes between `connect_wifi()` and `disconnect_wifi()` functions.

```python
# Get the current IP configuration of the interface
config = wifi.ifconfig()

# Print the configuration
print("Wi-Fi Configuration:")
print(f"IP address: \t{config[0]}")
print(f"Subnet mask:\t{config[1]}")
print(f"Gateway: \t{config[2]}")
print(f"DNS server:\t{config[3]}")
```

Apart from the IP configuration obtained using `ifconfig()`, you can also retrieve information such as:

**Signal strength (RSSI):**

```python
rssi = wifi.status("rssi")
print("Signal strength (RSSI):", rssi)
```

This will print the signal strength in dBm.

**MAC address:**

```python
mac_address = wifi.config('mac')
print("MAC address:", ':'.join(['{:02x}'.format(b) for b in mac_address]))
```

This code will print the MAC address of the ESP32.

**Is connected:**

```python
is_connected = wifi.isconnected()
print("Is connected:", is_connected)
```

This will print `True` if the ESP32 is connected to a Wi-Fi network, and `False` otherwise.

## ThingSpeak online platform

ThingSpeak is an Internet of Things (IoT) platform that allows you to collect, analyze, and visualize data from your connected devices. It provides APIs for storing and retrieving data, making it easy to integrate IoT devices into your projects. One common use case for ThingSpeak is to store and display sensor data.

1. Use breadboard, jumper wires, and connect I2C [DHT12](../../docs/dht12_manual.pdf) sensor to ESP32 GPIO pins as follows: SDA - GPIO 21, SCL - GPIO 22, VCC - 3.3V, GND - GND.

   > **Note:** Connect the components on the breadboard only when the supply voltage/USB is disconnected! There is no need to connect external pull-up resistors on the SDA and SCL pins, because the internal ones is used.

   ![firebeetle_pinout](../03-gpio/images/DFR0478_pinout.png)

2. Create a ThingSpeak Account: If you don't have a ThingSpeak account, sign up at [ThingSpeak](https://thingspeak.com/).

3. Create a Channel: After logging in, create a new channel. A channel is where you will store your sensor data and you can create up to four channels.

4. Get Channel API Key: In your channel settings, you'll find an Write API Key. This key is used to authenticate your device when sending data to ThingSpeak.

5. Write a MicroPython script that reads data from the DHT12 sensor and sends it to ThingSpeak. Use the `urequests` library to make HTTP requests.

TBD





















```python
from machine import Pin, I2C
import network
import urequests  # Network Request Module
from time import sleep


def connect_wifi():
    from time import sleep_ms

    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PSWD)
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")


def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


def read_dht12_sensor():
    # Read 5 bytes from addr. 0 from peripheral with 7-bit address 0x5c
    led.on()
    i2c.readfrom_mem_into(0x5c, 0, buf)
    led.off()

    # Check the checksum
    if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
        raise Exception("Checksum error")


# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
THINGSPEAK_API_KEY = "<THINGSPEAK WRITE API KEY>"

# Create Station interface
sta_if = network.WLAN(network.STA_IF)

# Create I2C peripheral at frequency of 100 kHz
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Status LED
led = Pin(2, Pin.OUT)

# Create an array of 5 bytes (2x humidity, 2x temperature, 1x checksum)
buf = bytearray(5)

# Forever loop
while True:
    read_dht12_sensor()

    # Put data together
    humi = buf[0] + (buf[1]*0.1)
    temp = buf[2] + (buf[3]*0.1)
    print(f"Temperature: {temp} C\tHumidity: {humi} %")

    connect_wifi()

    # Send data using a POST request
    request = urequests.post(
        'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_API_KEY,
        json={"field1": temp, "field2": humi},
        headers={"Content-Type": "application/json"})
    print(f"Request #{request.text} sent")
    request.close()

    disconnect_wifi()

    # Put device to sleep for 60 seconds
    sleep(60)
```

6. Go to your ThingSpeak channel to view the data being sent by your ESP32.











## NTP

```python

from machine import RTC
import network
import ntptime
from time import localtime, sleep


def connect_wifi():
    from time import sleep_ms

    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")

        # Activate station/Wi-Fi client interface
        sta_if.active(True)

        # Connect
        sta_if.connect(WIFI_SSID, WIFI_PSWD)

        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)

        print(" Connected")


def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)

    if not sta_if.isconnected():
        print("Disconnected")


# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
UTC_OFFSET = 2  # CEST is UTC+2:00

# Create an independent clock object
rtc = RTC()

# Create Station interface
sta_if = network.WLAN(network.STA_IF)
connect_wifi()

# Get UTC time from NTP server (pool.ntp.org) and store it
# to internal RTC
ntptime.settime()

# Display UTC (Coordinated Universal Time / Temps Universel Coordonné)
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print(f"UTC Time: {year}-{month}-{day} {hrs}:{mins}:{secs}")

# Get epoch time in seconds (for timezone update)
sec = ntptime.time()

disconnect_wifi()

# Update your epoch time in seconds and store in to internal RTC
sec = int(sec + UTC_OFFSET * 60 * 60)
(year, month, day, hrs, mins, secs, wday, yday) = localtime(sec)
rtc.datetime((year, month, day, wday, hrs, mins, secs, 0))

print(f"Local RTC time: UTC+{UTC_OFFSET}:00")

# Forever loop
while True:
    # Read values from internal RTC
    (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
    print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")

    # Delay 30 seconds
    sleep(30)
```
