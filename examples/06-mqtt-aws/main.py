# https://blog.caarels.com/posts/microPython_coreIOT_ptI/
# https://aws.amazon.com/blogs/iot/using-micropython-to-get-started-with-aws-iot-core/
# https://networklessons.com/cisco/evolving-technologies/connect-esp32-micropython-to-aws-iot
# https://esp32io.com/tutorials/esp32-aws-iot
# https://how2electronics.com/connecting-esp32-to-amazon-aws-iot-core-using-mqtt/

import time
import network
import ssl
from umqtt.simple import MQTTClient

# Configuration
WIFI_SSID = "YOUR-WIFI"
WIFI_PASSWORD = "YOUR-PASSWORD"
AWS_ENDPOINT = "YOUR-ENDPOINT.amazonaws.com"
AWS_CLIENT_ID = "ESP32"
AWS_TOPIC = "esp32/pub"

# Paths to the certificates and private key
CA_CERT_PATH = "/AmazonRootCA1.pem"
CLIENT_CERT_PATH = "/certificate.pem.crt"
PRIVATE_KEY_PATH = "/private.pem.key"

# Connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi:', wlan.ifconfig())

def create_ssl_context():
    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Load the CA certificate
    ssl_context.load_verify_locations(cafile=CA_CERT_PATH)

    # Load the client certificate and private key
    ssl_context.load_cert_chain(certfile=CLIENT_CERT_PATH, keyfile=PRIVATE_KEY_PATH)
    return ssl_context

def publish_to_aws():
    try:
        while True:
            # Read sensor data
            # dht_sensor.measure()
            # temperature = dht_sensor.temperature()
            # humidity = dht_sensor.humidity()
            temperature = 23.5
            humidity = 33.3

            ssl_context = create_ssl_context()

            # Initialize MQTT client
            mqtt_client = MQTTClient(
                client_id=AWS_CLIENT_ID,
                server=AWS_ENDPOINT,
                port=8883,
                keepalive=3600,
                ssl=ssl_context
            )

            # Connect to AWS
            mqtt_client.connect()
            print("Connected to {} MQTT Broker".format(AWS_ENDPOINT))

            # Prepare the MQTT message
            message = '{{"temperature": {}, "humidity": {}}}'.format(temperature, humidity)
            # Publish message to AWS
            mqtt_client.publish(AWS_TOPIC, message)
            print("- topic:", AWS_TOPIC)
            print("- payload:", message)

            mqtt_client.disconnect()
            print("Disconnected from AWS IoT")

            # Wait 60 seconds before the next reading
            time.sleep(60)

    except Exception as e:
        print("Error:", e)

# Main function
def main():
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    publish_to_aws()

# Run the main function
if __name__ == "__main__":
    main()
