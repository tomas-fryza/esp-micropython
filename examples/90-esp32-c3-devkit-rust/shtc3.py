from machine import I2C
import time


class SHTC3:
    ADDR = 0x70

    CMD_SLEEP = b"\xb0\x98"
    CMD_WAKEUP = b"\x35\x17"
    CMD_MEASURE = b"\x5c\x24"

    def __init__(self, i2c):
        self.i2c = i2c

    # -------------------------
    # Low-level commands
    # -------------------------
    def wake(self):
        self.i2c.writeto(self.ADDR, self.CMD_WAKEUP)

    def sleep(self):
        self.i2c.writeto(self.ADDR, self.CMD_SLEEP)

    def measure(self):
        self.i2c.writeto(self.ADDR, self.CMD_MEASURE)

    # -------------------------
    # CRC
    # -------------------------
    @staticmethod
    def crc8(data):
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc

    # -------------------------
    # Raw read with retry
    # -------------------------
    def _read_raw(self, retries=3):
        for _ in range(retries):
            try:
                raw = bytearray(6)
                self.i2c.readfrom_into(self.ADDR, raw)
                return raw
            except OSError:
                time.sleep_ms(5)
        raise OSError("SHTC3 read failed")

    # -------------------------
    # Decode + validate
    # -------------------------
    def _decode(self, raw):
        # Humidity MSB
        # Humidity LSB
        # Humidity CRC checksum
        # Temperature MSB
        # Temperature LSB
        # Temperature CRC checksum

        hum_raw = raw[0:2]
        hum_crc = raw[2]

        tmp_raw = raw[3:5]
        tmp_crc = raw[5]

        if self.crc8(hum_raw) != hum_crc:
            raise ValueError("Humidity CRC error")

        if self.crc8(tmp_raw) != tmp_crc:
            raise ValueError("Temperature CRC error")

        hum = (raw[0] << 8) | raw[1]
        tmp = (raw[3] << 8) | raw[4]

        humidity = ((625 * hum) >> 12) / 100.0
        temperature = (((4375 * tmp) >> 14) - 4500) / 100.0

        return temperature, humidity

    # -------------------------
    # High-level API
    # -------------------------
    def read(self, retries=3):
        for _ in range(retries):
            try:
                self.wake()
                time.sleep_ms(5)

                self.measure()
                time.sleep_ms(15)

                raw = self._read_raw()

                self.sleep()
                time.sleep_ms(2)

                return self._decode(raw)

            except (OSError, ValueError):
                time.sleep_ms(10)

        raise RuntimeError("SHTC3 measurement failed after retries")
