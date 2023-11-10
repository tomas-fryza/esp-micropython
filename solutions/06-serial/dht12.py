"""
MicroPython Aosong DHT12 I2C driver
https://pypi.org/project/micropython-dht12/

Updated: Tomas Fryza

2023-11-10: Scanning method added
"""

SENSOR_ADDR = 0x5c
SENSOR_HUMI_REG = 0
SENSOR_TEMP_REG = 2
SENSOR_CHECKSUM = 4


class DHTBaseI2C:
    def __init__(self, i2c, addr=SENSOR_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)
        # self.scan()

    def measure(self):
        buf = self.buf
        self.i2c.readfrom_mem_into(self.addr, SENSOR_HUMI_REG, buf)
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
