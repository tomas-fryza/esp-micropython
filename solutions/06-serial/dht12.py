"""
MicroPython Aosong DHT12 I2C driver

This library lets you communicate with an Aosong DHT12
temperature and humidity sensor over I2C.

Authors:
- Mike Causer, https://pypi.org/project/micropython-dht12/
- Tomas Fryza

2024-11-02: Read values method added
2023-11-10: Scanning method added
"""

SENSOR_ADDR = 0x5c


class DHTBaseI2C:
    def __init__(self, i2c, addr=SENSOR_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
        self.scan()

    def measure(self):
        buf = self.buf
        # Read 5 bytes from address 0 to the buffer
        self.i2c.readfrom_mem_into(self.addr, 0, buf)
        if (buf[0] + buf[1] + buf[2] + buf[3]) & 0xff != buf[4]:
            raise Exception(f"`{hex(SENSOR_ADDR)}` checksum error")

    def scan(self):
        addrs = self.i2c.scan()
        if SENSOR_ADDR not in addrs:
            raise Exception(f"`{hex(SENSOR_ADDR)}` is not detected")


class DHT12(DHTBaseI2C):
    def humidity(self):
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

    def read_values(self):
        """
        Read temperature and humidity from the sensor.

        :returns: A tuple containing the temperature
                  (float) and humidity (float) values.
        :rtype: tuple
        """
        self.measure()
        return self.temperature(), self.humidity()
