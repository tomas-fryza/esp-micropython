# https://blog.caarels.com/posts/microPython_coreIOT_ptI/
# https://aws.amazon.com/blogs/iot/using-micropython-to-get-started-with-aws-iot-core/
# https://networklessons.com/cisco/evolving-technologies/connect-esp32-micropython-to-aws-iot

import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient

#Enter your wifi SSID and password below.
wifi_ssid = "WIRELESS_SSID"
wifi_password = "WIRELESS_PASSWORD"

#Enter your AWS IoT endpoint. You can find it in the Settings page of
#your AWS IoT Core console. 
#https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html 
# You can test in Terminal:
# ping xxxxx.eu-central-1.amazonaws.com
aws_endpoint = b'xxxxx.eu-central-1.amazonaws.com'

#If you followed the blog, these names are already set.
thing_name = "ESP32"
client_id = "ESP32"
private_key = "private.pem.key"
private_cert = "certificate.pem.crt"

#Read the files used to authenticate to AWS IoT Core
with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()

#These are the topics we will subscribe to. We will publish updates to /update.
#We will subscribe to the /update/delta topic to look for changes in the device shadow.
topic_pub = thing_name + "/update"
topic_sub = thing_name + "/update/delta"
ssl_params = {"key":key, "cert":cert, "server_side":False}

#Define pins for LED and light sensor. In this example we are using a FeatherS2.
#The sensor and LED are built into the board, and no external connections are required.
# light_sensor = machine.ADC(machine.Pin(4))
# light_sensor.atten(machine.ADC.ATTN_11DB)
led = machine.Pin(9, machine.Pin.OUT)
info = os.uname()

#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)
    if message['state']['led']:
        led_state(message)
    print("Done")

def led_state(message):
    led.value(message['state']['led']['onboard'])

#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    mqtt.subscribe(topic_sub)
except:
    print("Unable to connect to MQTT.")


while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except:
        print("Unable to check for messages.")

    mesg = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
#                 "sensors": {
#                     "light": light_sensor.read()
#                 },
                "led": {
                    "onboard": led.value()
                }
            }
        }
    })

#Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)
