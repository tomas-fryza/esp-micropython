import network
import mywifi
import urequests  # Network Request Module

# Network settings
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PSWD = "<YOUR WIFI PASSWORD>"
API_KEY = "<OpenWeatherMap API KEY>"
CITY = "Brno,cz"


def read_openweathermap():
    API_URL = "http://api.openweathermap.org/data/2.5/"

    # Select GET or POST request
    # GET request
    request_url = f"{API_URL}weather?appid={API_KEY}&q={CITY}&units=metric"
    response = urequests.get(request_url)

    print("Response from OpenWeatherMap:")
    print(response.text)
    response.close()


# Create Station interface
wifi = network.WLAN(network.STA_IF)
mywifi.connect(wifi, WIFI_SSID, WIFI_PSWD)
read_openweathermap()
mywifi.disconnect(wifi)
