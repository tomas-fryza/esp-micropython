"""
This module provides a MicroPython driver for the Aosong DHT12
temperature and humidity sensor, which communicates over I2C.
It includes classes and methods for reading temperature and
humidity data from the sensor.

Classes
-------
- ``DHTBaseI2C`` : Base class for handling low-level I2C communication with the DHT12 sensor.
- ``DHT1`` : Extends `DHTBaseI2C` to provide methods for reading temperature and humidity values.

Attributes
----------
- ``SENSOR_ADDR`` : The default I2C address (0x5c) of the DHT12 sensor.

Example
-------
.. code-block:: python

    from dht12 import DHT12
    from machine import I2C, Pin

    # Initialize I2C interface
    i2c = I2C(0, scl=Pin(22), sda=Pin(21))

    # Create an instance of the DHT12 sensor
    sensor = DHT12(i2c)

    # Read and print temperature and humidity values
    temperature, humidity = sensor.read_values()
    print(f"Temperature: {temperature} °C, Humidity: {humidity} %")

Authors
-------
- Mike Causer, `PyPI <https://pypi.org/project/micropython-dht12/>`_
- Tomas Fryza

Modification history
--------------------
- **2024-11-11** : Added Sphinx comments.
- **2024-11-02** : Added `read_values` method.
- **2023-11-10** : Added `scan` method.
"""

SENSOR_ADDR = 0x5c


class DHTBaseI2C:
    def __init__(self, i2c, addr=SENSOR_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
        self.scan()

    def measure(self):
        """
        Reads 5 bytes of data from the DHT12 sensor's memory and performs
        a checksum validation to ensure data integrity. The retrieved data
        is stored in the buffer (`self.buf`). If the checksum validation fails,
        an exception is raised.

        :raises Exception: If the checksum validation fails, indicating potential
                           data corruption.

        :Example:

            .. code-block:: python

                sensor = DHT12(i2c)
                try:
                    sensor.measure()
                    print("Data read successfully.")
                except Exception as e:
                    print("Checksum error:", e)
        """
        buf = self.buf
        # Read 5 bytes from address 0 to the buffer
        self.i2c.readfrom_mem_into(self.addr, 0, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception(f"`{hex(SENSOR_ADDR)}` checksum error")

    def scan(self):
        """
        Checks if the DHT12 sensor is available on the I2C bus by scanning
        for its specified address (`SENSOR_ADDR`). If the sensor is not
        found, it raises an exception.

        :raises Exception: If the sensor address (`SENSOR_ADDR`) is not
                           detected on the I2C bus.

        :Example:

            .. code-block:: python

                sensor = DHT12(i2c)
                try:
                    sensor.scan()
                    print("Sensor detected.")
                except Exception as e:
                    print(e)
        """
        addrs = self.i2c.scan()
        if SENSOR_ADDR not in addrs:
            raise Exception(f"`Sensor {hex(SENSOR_ADDR)}` not detected")


class DHT12(DHTBaseI2C):
    def humidity(self):
        """
        Calculates and returns the humidity as a floating-point value,
        using data previously read into the buffer (`self.buf`) by the
        `measure` method. 

        :returns: The current humidity as a percentage.

        :Example:

            .. code-block:: python

                sensor = DHT12(i2c)
                sensor.measure()  # Read data from sensor
                humidity = sensor.humidity()
                print(f"Humidity: {humidity} %")
        """
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        """
        Calculates and returns the temperature in degrees Celsius as a
        floating-point value, using data stored in the buffer (`self.buf`)
        by the `measure` method. It interprets both positive and negative
        temperatures.

        :returns: The current temperature in degrees Celsius.

        :Example:

            .. code-block:: python

                sensor = DHT12(i2c)
                sensor.measure()  # Read data from sensor
                temperature = sensor.temperature()
                print(f"Temperature: {temperature} °C")
        """
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

    def read_values(self):
        """
        Read temperature and humidity from the sensor.

        :returns: A tuple containing the temperature (float)
                  and humidity (float) values.
        """
        self.measure()
        return self.temperature(), self.humidity()
