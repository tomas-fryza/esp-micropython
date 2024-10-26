"""
Example of GET/POST requests

This script demonstrates how to make GET and POST requests
using MicroPython. It connects to a specified Wi-Fi network
and retrieves data from various APIs.

APIs used:
  - Joke API: https://v2.jokeapi.dev/
  - Cat Fact API: https://catfact.ninja/
  - Time API: https://timeapi.io/
  - CoinGecko API: https://coingecko.com/

Other APIs (api-key needed):
   https://quotes.rest/
   https://openweathermap.org/
   https://openaq.org/
   https://www.iqair.com/world-air-quality

Components:
  - ESP32 microcontroller

Authors: Tomas Fryza
Creation Date: 2024-10-25
Last Modified: 2024-10-26
"""

import network
import my_wifi
import config
import urequests  # Network Request Module
import time

# Create Station interface
wifi = network.WLAN(network.STA_IF)
print("Start using Wi-Fi. Press `Ctrl+C` to stop")

try:
    # Forever loop
    while True:
        my_wifi.connect(wifi, config.SSID, config.PSWD)


        # GET requests
        API_URL = "https://catfact.ninja/fact"

        # API_URL = "https://v2.jokeapi.dev/joke/Programming"

        # List of GET/POST methods: https://timeapi.io/swagger/index.html
        # API_URL = "https://timeapi.io/api/time/current/zone?timeZone=Europe/Prague"

        # Fetch the current price of cryptocurrencies in various currencies
        # https://docs.coingecko.com/reference/simple-price
        # API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"

        print("Method used: GET")
        request_url = f"{API_URL}"
        response = urequests.get(request_url)


        # POST requests
        # List of GET/POST methods: https://timeapi.io/swagger/index.html
        # API_URL = "https://timeapi.io/api/conversion/converttimezone"

        # print("Method used: POST")
        # request_url = f"{API_URL}"
        # json = {"fromTimeZone": "Europe/Prague",
        #         "dateTime": "2024-10-26 15:33:00",
        #         "toTimeZone": "America/Los_Angeles",
        #         "dstAmbiguity": ""}
        # headers = {"Content-Type": "application/json"}
        # response = urequests.post(request_url, json=json, headers=headers)


        print("Response:")
        print(response.text)
        response.close()

        my_wifi.disconnect(wifi)
        time.sleep(30)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    my_wifi.disconnect(wifi)
