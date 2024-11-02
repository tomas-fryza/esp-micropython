"""
MicroPython Weather Fetcher
===========================

This script connects to a Wi-Fi network and fetches current
weather data for a specified city from the OpenWeatherMap API.
It prints out relevant weather information such as temperature,
wind speed, and humidity.

Notes: 
- Get your API_KEY from https://openweathermap.org/

Components:
- ESP32-based board

Author: Tomas Fryza

Creation date: 2023-10-26
Last modified: 2024-11-02
"""

import network
import my_wifi
import config
import urequests
import ujson

API_KEY = "OpenWeatherMap_API_KEY"
CITY = "Brno,cz"


def read_openweathermap():
    """Fetches weather data from OpenWeatherMap."""
    API_URL = "http://api.openweathermap.org/data/2.5/"

    # Make the GET request
    request_url = f"{API_URL}weather?appid={API_KEY}&q={CITY}&units=metric"
    response = urequests.get(request_url)

    # Check if the request was successful
    if response.status_code == 200:
        print("")
        print("Response from OpenWeatherMap:")
        print(response.text)
        data = ujson.loads(response.text)
        
        print("")
        print(f"{data["name"]}, {data["sys"]["country"]}", end="")
        print(f" (latitude: {data["coord"]["lat"]}, longitude: {data["coord"]["lon"]})")
        print(f"{data["weather"][0]["main"]} ({data["weather"][0]["description"]})")
        print(f"Temperature: {data["main"]["temp"]}°C (feels like: {data["main"]["feels_like"]}°C)")
        print(f"Wind speed: {data["wind"]["speed"]} m/s ({data["wind"]["deg"]}°)")
        print(f"Pressure: {data["main"]["pressure"]} hPa")
        print(f"Humidity: {data["main"]["humidity"]} %")
        print("")
    else:
        print("Error:", response.status_code, response.text)

    # Close the response to free up resources
    response.close()


# Create Station interface
wifi = network.WLAN(network.STA_IF)
my_wifi.connect(wifi, config.SSID, config.PSWD)
read_openweathermap()
my_wifi.disconnect(wifi)
