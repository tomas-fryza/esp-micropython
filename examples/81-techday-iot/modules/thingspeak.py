import urequests

API_URL = "https://api.thingspeak.com/update"


def send(value1, value2, api_key):
    """
    Send two parameters to ThingSpeak.
    """

    # Select GET or POST request
    # Make the GET request
    request_url = f"{API_URL}?api_key={api_key}&field1={value1}&field2={value2}"
    try:
        response = urequests.get(request_url)
        # print("Status code:", response.status_code)
        print(f"ThingSpeak entry no.: {response.text}")
        response.close()
    except Exception as e:
        print("Error sending data:", e)
        response = urequests.get(request_url)

    # Make the POST request
    # request_url = f"{API_URL}?api_key={API_KEY}"
    # json = {"field1": value1, "field2": value2}
    # headers = {"Content-Type": "application/json"}
    # response = urequests.post(request_url, json=json, headers=headers)
    # print(f"ThingSpeak entry no.: {response.text}")
    # response.close()
