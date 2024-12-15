"""
MicroPython script to read data from a BME280 sensor and
publish it to ThingSpeak using MQTT.

Authors
-------
- Marcelo Rovai, `IoT Made Easy: ESP-MicroPython-MQTT-ThingSpeak <https://towardsdatascience.com/iot-made-easy-esp-micropython-mqtt-thingspeak-ce05eea27814>`_
- Mike Teachman, `MQTT protocol with Thingspeak using Micropython <https://github.com/miketeachman/micropython-mqtt-thingspeak/tree/master>`_
- Gunter Spanner, MicroPython for Microcontrollers, ISBN 978-3-89576-436-3
- Tomas Fryza

Modification history
--------------------
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

PUBLISH_TIME_SEC = 300

# MQTT parameters
BROKER_ADDRESS = "mqtt3.thingspeak.com"
MQTT_CLIENT_ID = "your_client_id"
MQTT_USERNAME = "your_mqtt_username"
MQTT_PASSWORD = "your_mqtt_password"
CHANNEL_ID = "your_thingspeak_channel_id"

# Setup I2C for BME280 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
bme = bme280.BME280(i2c)
T, RH, P, _ = bme.read_values()

# Wi-Fi Station interface
wifi = network.WLAN(network.STA_IF)
wifi_module.connect(wifi, config.SSID, config.PSWD)

# Setup MQTT client
# Note: Connection uses unsecure TCP (port 1883)
client = MQTTClient(
    server=BROKER_ADDRESS,
    client_id=MQTT_CLIENT_ID, 
    user=MQTT_USERNAME, 
    password=MQTT_PASSWORD, 
    ssl=False)
# MQTT topic
topic = "channels/{}/publish".format(CHANNEL_ID)

# Initialize previous sensor data
prev_T = T + 10  # Make sure the first readings are published
prev_RH = RH
prev_P = P

# Publish sensor data if changed
def publish_data(T, RH, P):
    global prev_T, prev_RH, prev_P

    # Check if the data has changed (ignore small fluctuations)
    # if (T != prev_T) or (RH != prev_RH) or (P != prev_P):
    if abs(T - prev_T) > 0.1 or abs(RH - prev_RH) > 1 or abs(P - prev_P) > 1:
        # Prepare payload
        payload = "field1={:.1f}&field2={:.1f}&field3={:.1f}".format(T, RH, P)

        try:
            client.connect()
            client.publish(topic, payload)
            client.disconnect()
            print(f"[I] Data published to topic: {topic}")

            # Update previous values after publishing
            prev_T = T
            prev_RH = RH
            prev_P = P
        except Exception as e:
            print(f"[E] Failed to publish data: {type(e).__name__}{e}")
    else:
        print("[I] No (small) changes in sensor data, skipping publish")

print("[I] Start publishing data to MQTT broker")
print("[I] Press `Ctrl+C` to stop")
print()

# Main loop to read and publish data
try:
    while True:
        # Read the sensor data
        T, RH, P, _ = bme.read_values()
        print(f"[BME280] temp(°C), humi(%), pres(hPa): {T:.1f}, {RH:.1f}, {P:.1f}")

        # Publish data if it has changed
        publish_data(T, RH, P)

        # Wait before next reading
        time.sleep(PUBLISH_TIME_SEC)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\r\n[I] Program stopped. Exiting...")

    # Optional cleanup code
    try:
        client.disconnect()
    except Exception as e:
        print(f"[E] Failed to disconnect from MQTT server {type(e).__name__}{e}")
    wifi_module.disconnect(wifi)
