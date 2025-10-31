# TODO: Check the algos:
# - https://github.com/Sensirion/gas-index-algorithm?utm_source=chatgpt.com
# - https://sensirion.com/media/documents/5FE8673C/61E96F50/Sensirion_Gas_Sensors_Datasheet_SGP41.pdf
# - https://sensirion.com/media/documents/02232963/6294E043/Info_Note_VOC_Index.pdf?utm_source=chatgpt.com

from machine import I2C, Pin
import utime, struct, math

class SGP41:
    """MicroPython driver for Sensirion SGP41 (VOC + NOx)."""

    class CRCException(Exception):
        pass

    class NotFoundException(Exception):
        pass

    DEFAULT_ADDR = 0x59

    CMD_CONDITIONING = 0x2612
    CMD_MEASURE_RAW = 0x2619
    CMD_SELF_TEST = 0x280E
    CMD_HEATER_OFF = 0x3615
    CMD_GET_SERIAL = 0x3682

    def __init__(self, i2c, addr=DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr
        if addr not in i2c.scan():
            raise self.NotFoundException("SGP41 not detected on I2C bus.")
        # algorithm state
        self.voc_index_state = 0.0
        self.nox_index_state = 0.0

    # --- CRC helper ---
    def __crc(self, msb, lsb):
        crc = 0xFF
        for b in [msb, lsb]:
            for _ in range(8):
                if (crc ^ b) & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
                crc &= 0xFF
                b <<= 1
                b &= 0xFF
        return crc

    def __check_crc(self, arr):
        if self.__crc(arr[0], arr[1]) != arr[2]:
            raise self.CRCException("CRC mismatch")

    def __write_command(self, cmd, data=None):
        cmd_bytes = struct.pack(">H", cmd)
        payload = cmd_bytes + data if data else cmd_bytes
        self.i2c.writeto(self.addr, payload)

    def __read_bytes(self, count):
        return self.i2c.readfrom(self.addr, count)

    # --- Sensor operations ---
    def execute_conditioning(self, humidity=0x8000, temperature=0x6666):
        paramh = struct.pack(">H", humidity)
        crch = self.__crc(paramh[0], paramh[1])
        paramt = struct.pack(">H", temperature)
        crct = self.__crc(paramt[0], paramt[1])
        data = paramh + bytes([crch]) + paramt + bytes([crct])
        self.__write_command(self.CMD_CONDITIONING, data)
        utime.sleep_ms(50)
        raw = self.__read_bytes(3)
        self.__check_crc(raw)
        return struct.unpack(">H", raw[:2])[0]

    def measure_raw(self, humidity=0x8000, temperature=0x6666):
        paramh = struct.pack(">H", humidity)
        crch = self.__crc(paramh[0], paramh[1])
        paramt = struct.pack(">H", temperature)
        crct = self.__crc(paramt[0], paramt[1])
        data = paramh + bytes([crch]) + paramt + bytes([crct])
        self.__write_command(self.CMD_MEASURE_RAW, data)
        utime.sleep_ms(50)
        raw = self.__read_bytes(6)
        self.__check_crc(raw[0:3])
        self.__check_crc(raw[3:6])
        voc_raw = struct.unpack(">H", raw[0:2])[0]
        nox_raw = struct.unpack(">H", raw[3:5])[0]
        return voc_raw, nox_raw

    def heater_off(self):
        self.__write_command(self.CMD_HEATER_OFF)
        utime.sleep_ms(1)

    def get_serial_number(self):
        self.__write_command(self.CMD_GET_SERIAL)
        utime.sleep_ms(1)
        data = self.__read_bytes(9)
        self.__check_crc(data[0:3])
        self.__check_crc(data[3:6])
        self.__check_crc(data[6:9])
        serial = struct.unpack(">HHH", bytes([data[0], data[1], data[3], data[4], data[6], data[7]]))
        return "-".join(["%04X" % s for s in serial])

    # --- VOC + NOx index algorithms ---
    def compute_voc_index(self, sraw_voc):
        """Approximate VOC Index computation from raw value."""
        # Normalize and smooth
        voc = (sraw_voc - 20000) / 1000.0
        self.voc_index_state = 0.98 * self.voc_index_state + 0.02 * voc

        x = self.voc_index_state + 1.0
        if x <= 0:
            x = 0.0001  # prevent math domain error
        index = max(0, min(500, 100 * math.log(x)))
        return round(index)

    def compute_nox_index(self, sraw_nox):
        """Approximate NOx Index computation from raw value."""
        nox = (sraw_nox - 15000) / 800.0
        self.nox_index_state = 0.97 * self.nox_index_state + 0.03 * nox

        x = self.nox_index_state + 1.0
        if x <= 0:
            x = 0.0001
        index = max(0, min(500, 120 * math.log(x)))
        return round(index)

# --- Example usage ---
if __name__ == "__main__":
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    sgp = SGP41(i2c)
    print("SGP41 initialized.")
    print("Serial:", sgp.get_serial_number())

    try:
        print("Conditioning...")
        for _ in range(5):
            voc_raw = sgp.execute_conditioning()
            print("VOC raw:", voc_raw)
            utime.sleep(1)

        while True:
            voc_raw, nox_raw = sgp.measure_raw()
            voc_idx = sgp.compute_voc_index(voc_raw)
            nox_idx = sgp.compute_nox_index(nox_raw)
            print("VOC raw:", voc_raw, "→ index:", voc_idx,
                  "| NOx raw:", nox_raw, "→ index:", nox_idx)
            utime.sleep(1)

    except KeyboardInterrupt:
        sgp.heater_off()
        print("\nMeasurement stopped by user. Heater turned off.")
