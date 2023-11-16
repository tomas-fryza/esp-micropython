import gc  # Garbage Collector interface (Memory management)
gc.collect()


def connect(wifi, ssid, password):
    """
    Connect to Wi-Fi network.

    Activates the Wi-Fi interface, connects to the specified network,
    and waits until the connection is established.

    :return: None
    """
    from time import sleep_ms

    if not wifi.isconnected():
        wifi.active(True)
        wifi.connect(ssid, password)

        symbols = ["/", "-", "\\", "|"]
        i = 0
        while not wifi.isconnected():
            print(f"Connecting to {ssid}... {symbols[i]}", end="\r")
            sleep_ms(100)
            i = (i + 1) % 4
        print(f"Connecting to {ssid}... Done")
    else:
        print("Already connected")


def disconnect(wifi):
    """
    Disconnect from Wi-Fi network.

    Deactivates the Wi-Fi interface if active and checks if
    the device is not connected to any Wi-Fi network.

    :return: None
    """
    if wifi.active():
        wifi.active(False)

    if not wifi.isconnected():
        print("Disconnected")
