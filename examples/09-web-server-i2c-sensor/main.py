"""Main file of the web server for the DHT12 sensor data.

File contains web server sending DHT12 sensor data to web page.

NOTES:
    * Set your Wi-Fi SSID and password in `boot.py`
    * Connect DHT12 sensor to I2C pins:
        DHT12  ESP32 ESP8266 ESP32-CAM ESP32C3
        SCL     22      5       15        8
        SDA     21      4       13       10
        +      3.3V    3.3V    3.3V     3.3V
        -      GND     GND     GND      GND

    * Save copy of both files (`boot.py` and `main.py`) to
      ESP device and press on-board reset button
    * Put IP address from the Shell to your web browser

Inspired by:
    * https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
    * https://fontawesome.com/icons
"""


def read_dht12_sensor():
    # Read 5 bytes from addr. 0 from peripheral with 7-bit address 0x5c
    led.on()
    i2c.readfrom_mem_into(0x5c, 0, buf)
    led.off()

    # Checksum
    if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
        raise Exception("Checksum error")


def read_raw_temperature():
    import esp32
    temp_f = esp32.raw_temperature()
    temp_c = (temp_f-32) * (5/9)
    return(round(temp_c, 1))


def web_page():
    html_code = """<!DOCTYPE HTML><html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }
        h2 { font-size: 3.0rem; }
        p { font-size: 3.0rem; }
        .units { font-size: 1.2rem; }
        .dht-labels {
            font-size: 1.5rem;
            vertical-align:middle;
            padding-bottom: 15px;
        }
    </style>
</head>
<body>
    <h2>ESP DHT Server</h2>

    <p><i class="fas fa-thermometer-quarter" style="color:#008000;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&#186;C</sup></p>

    <p><i class="fas fa-thermometer-half" style="color:#dd0000;"></i> 
    <span class="dht-labels">ESP Temperature</span> 
    <span>"""+str(temp_c)+"""</span>
    <sup class="units">&#186;C</sup></p>

    <p><i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span>"""+str(humi)+"""</span>
    <sup class="units">%</sup></p>
</body>
</html>"""
    return html_code


# Create I2C peripheral at frequency of 100 kHz
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
# Create an array of 5 bytes (2x humidity, 2x temperature, 1x checksum)
buf = bytearray(5)

# Status LED
led = Pin(2, Pin.OUT)

# Create TCP/IP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

# Forever loop
while True:
    # Accept a new connection
    conn, address = s.accept()

    # Receive data from the remote socket; maximum size is 512 bytes
    request = conn.recv(512)
    print(f"Request received ({len(request)} bytes) from {address}")
    print(request.decode())

    # Get sensor data
    read_dht12_sensor()
    temp_c = read_raw_temperature()
    humi = buf[0] + (buf[1]*0.1)
    temp = buf[2] + (buf[3]*0.1)
    print(f"Temperature: {temp} C\tHumidity: {humi} %")

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
