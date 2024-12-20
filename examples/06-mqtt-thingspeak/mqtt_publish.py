"""
MicroPython script to read data from a BME280 sensor and
publish it to ThingSpeak using MQTT (Message Queue Telemetry
Transport Protocol).

Authors
-------
- Marcelo Rovai, `IoT Made Easy: ESP-MicroPython-MQTT-ThingSpeak <https://towardsdatascience.com/iot-made-easy-esp-micropython-mqtt-thingspeak-ce05eea27814>`_
- Mike Teachman, `MQTT protocol with Thingspeak using Micropython <https://github.com/miketeachman/micropython-mqtt-thingspeak/tree/master>`_
- Gunter Spanner, MicroPython for Microcontrollers, ISBN 978-3-89576-436-3
- Tomas Fryza

Modification history
--------------------
- **2024-12-16** : print_log function added.
- **2024-12-14** : Example created and tested.
"""

from machine import I2C
from machine import Pin
import time
import bme280
import network
import wifi_module
import config
from umqtt.robust import MQTTClient
import mqtt_credentials as mc
import sys

PUBLISH_TIME_SEC = 60  # 300

# MQTT parameters
BROKER_ADDRESS = "mqtt3.thingspeak.com"
# MQTT_USERNAME = "your_mqtt_username"
# MQTT_CLIENT_ID = "your_client_id"
# MQTT_PASSWORD = "your_mqtt_password"
# CHANNEL_ID = "your_thingspeak_channel_id"


# Function to print log messages with elapsed time and log level
def print_log(level, message):
    # Get the current time in milliseconds since the application start
    elapsed_time = time.ticks_ms() - start_time

    # Format the log message
    if level == "E":
        level = "\x1b[31m" + level
        message = message + "\x1b[0m"
    log_message = f"{level} ({elapsed_time}) {message}"

    # Print the formatted log message to the serial monitor
    print(log_message)


# Publish sensor data if changed
def publish_data(T, RH, P):
    global prev_T, prev_RH, prev_P

    # Check if the data has changed (ignore small fluctuations)
    if abs(T-prev_T) > 0.1 or abs(RH-prev_RH) > 1 or abs(P-prev_P) > 1:
        # Prepare payload
        payload = "field1={:.1f}&field2={:.1f}&field3={:.1f}".format(T, RH, P)

        try:
            client.connect()
            client.publish(topic, payload)
            client.disconnect()
            print_log("I", "mqtt: Data published to channel: {}".format(topic))

            # Update previous values after publishing
            prev_T = T
            prev_RH = RH
            prev_P = P
        except Exception as e:
            print_log("E", "mqtt: Failed to publish data: {}{}".formagt(type(e).__name__, e))
    else:
        print_log("I", "mqtt: No/small changes, skipping publish")


# Initialize start time for log system
start_time = time.ticks_ms()

# Setup I2C for BME280 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
bme = bme280.BME280(i2c)
T, RH, P, _ = bme.read_values()

# Wi-Fi Station interface
wifi = network.WLAN(network.STA_IF)
if not wifi_module.connect(wifi, config.SSID, config.PSWD):
    sys.exit()

# Setup MQTT client and topic
# Note: Connection uses unsecure TCP (port 1883)
client = MQTTClient(
    server=BROKER_ADDRESS,
    client_id=mc.MQTT_CLIENT_ID, 
    user=mc.MQTT_USERNAME, 
    password=mc.MQTT_PASSWORD, 
    ssl=False)
topic = "channels/{}/publish".format(mc.CHANNEL_ID)

# Initialize previous sensor data
prev_T = T + 10  # Make sure the first readings are published
prev_RH = RH
prev_P = P

print_log("I", "main: Start publishing data to MQTT broker")
print_log("I", "main: Press `Ctrl+C` to stop")

# Main loop to read and publish data
try:
    while True:
        # Read the sensor data
        T, RH, P, _ = bme.read_values()
        print_log("I", "bme280: temp(°C), humi(%), pres(hPa): {:.1f}, {:.1f}, {:.1f}".format(T, RH, P))

        # Publish data if it has changed
        publish_data(T, RH, P)

        # Wait before next reading
        time.sleep(PUBLISH_TIME_SEC)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print_log("I", "main: Program stopped. Exiting...")

    # Optional cleanup code
    wifi_module.disconnect(wifi)
