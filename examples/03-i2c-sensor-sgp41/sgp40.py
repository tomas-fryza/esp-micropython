from machine import I2C, Pin
import utime
import struct
import math

class SGP40:

    class NotFoundException(Exception):
        pass

    class NotSupportedException(Exception):
        pass

    class CRCException(Exception):
        pass

    MEASUREMENT_RAW = 0x260f
    MEASUREMENT_TEST = 0x280e
    HEATER_OFF = 0x3615
    RESET = 0x0006

    GET_SERIAL_ID = 0x3682
    GET_FEATURESET = 0x202f

    # Generated using
    # crc_table = []
    # for crc in range(256):
    #     for crc_bit in range(8):
    #         if crc & 0x80:
    #             crc = (crc << 1) ^ CRC8_POLYNOMIAL;
    #         else:
    #             crc = (crc << 1);
    #         crc = crc%256
    #     crc_table.append(crc)

    CRC_TABLE = [
        0, 49, 98, 83, 196, 245, 166, 151, 185, 136, 219, 234, 125, 76, 31, 46,
        67, 114, 33, 16, 135, 182, 229, 212, 250, 203, 152, 169, 62, 15, 92, 109,
        134, 183, 228, 213, 66, 115, 32, 17, 63, 14, 93, 108, 251, 202, 153, 168,
        197, 244, 167, 150, 1, 48, 99, 82, 124, 77, 30, 47, 184, 137, 218, 235,
        61, 12, 95, 110, 249, 200, 155, 170, 132, 181, 230, 215, 64, 113, 34, 19,
        126, 79, 28, 45, 186, 139, 216, 233, 199, 246, 165, 148, 3, 50, 97, 80,
        187, 138, 217, 232, 127, 78, 29, 44, 2, 51, 96, 81, 198, 247, 164, 149,
        248, 201, 154, 171, 60, 13, 94, 111, 65, 112, 35, 18, 133, 180, 231, 214,
        122, 75, 24, 41, 190, 143, 220, 237, 195, 242, 161, 144, 7, 54, 101, 84,
        57, 8, 91, 106, 253, 204, 159, 174, 128, 177, 226, 211, 68, 117, 38, 23,
        252, 205, 158, 175, 56, 9, 90, 107, 69, 116, 39, 22, 129, 176, 227, 210,
        191, 142, 221, 236, 123, 74, 25, 40, 6, 55, 100, 85, 194, 243, 160, 145,
        71, 118, 37, 20, 131, 178, 225, 208, 254, 207, 156, 173, 58, 11, 88, 105,
        4, 53, 102, 87, 192, 241, 162, 147, 189, 140, 223, 238, 121, 72, 27, 42,
        193, 240, 163, 146, 5, 52, 103, 86, 120, 73, 26, 43, 188, 141, 222, 239,
        130, 179, 224, 209, 70, 119, 36, 21, 59, 10, 89, 104, 255, 206, 157, 172
        ]

    def __init__(self, i2c, addr=0x59):
        self.i2c = i2c
        self.addr = addr
        if not addr in i2c.scan():
            raise self.NotFoundException
        self._voc_mean = 0.0
        self._voc_initialized = False

    # -----------------------------
    # VOC Algorithm Implementation
    # -----------------------------
    def _voc_algorithm(self, raw_voc):
        """Simplified adaptive algorithm for MicroPython."""
        # Normalize around a typical baseline (~20000)
        voc_norm = (raw_voc - 20000) / 4000.0

        if not self._voc_initialized:
            self._voc_mean = voc_norm
            self._voc_initialized = True

        alpha = 0.05  # smoothing factor
        self._voc_mean = (1 - alpha) * self._voc_mean + alpha * voc_norm

        # Compute simple scaled index
        voc_index = int(100 + 100 * (voc_norm - self._voc_mean))
        voc_index = max(0, min(voc_index, 500))  # clamp 0–500
        return voc_index

    def measure_voc_index(self, humidity=50, temperature=25):
        """
        Measure raw VOC and return computed VOC index.

        VOC Index to Air Quality Mapping:

        VOC Index    Air Quality
        0–100        Excellent
        100–200      Good
        200–300      Moderate
        300–400      Poor
        400–500      Very Poor
        """
        raw = self.measure_raw(humidity, temperature)
        voc_index = self._voc_algorithm(raw)
        return raw, voc_index

    def measure_raw(self, humidity=50, temperature=25):
        paramh = struct.pack(">H", math.ceil(humidity * 0xffff / 100))
        crch = self.__crc(paramh[0], paramh[1])
        paramt = struct.pack(">H", math.ceil((temperature + 45) * 0xffff / 175))
        crct = self.__crc(paramt[0], paramt[1])
        data = paramh + bytes([crch]) + paramt + bytes([crct])
        self.i2c.writeto_mem(self.addr, self.MEASUREMENT_RAW, data, addrsize=16)
        utime.sleep_ms(30)
        raw = self.i2c.readfrom(self.addr, 3)
        self.__check_crc(raw)
        return struct.unpack('>H', raw[:2])[0]

    def measure_test(self):
        raw = self.__read_bytes(self.MEASUREMENT_TEST, 3, 250000)
        self.__check_crc(raw)
        return struct.unpack('>H', raw[:2])[0]

    def reset(self):
        self.__write_command(self.RESET)

    def heater_off(self):
        self.__write_command(self.HEATER_OFF)

    def get_serial_id(self):
        data = self.__read_bytes(self.GET_SERIAL_ID, 6, 500)
        serial_hex = '-'.join(['%02X' % b for b in data])
        return serial_hex

    def __write_command(self, cmd):
        bcmd = struct.pack('>H', cmd)
        self.i2c.writeto(self.addr, bcmd)

    def __read_bytes(self, cmd, count, pause):
        self.__write_command(cmd)
        utime.sleep_us(pause)
        return self.i2c.readfrom(self.addr, count)

    def __check_crc(self, arr):
        assert (len(arr) == 3)
        if self.__crc(arr[0], arr[1]) != arr[2]:
            raise self.CRCException

    def __crc(self, msb, lsb):
        crc = 0xff
        crc ^= msb
        crc = self.CRC_TABLE[crc]
        if lsb is not None:
            crc ^= lsb
            crc = self.CRC_TABLE[crc]
        return crc


if __name__ == "__main__":

    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
    sensor = SGP40(i2c)
    print("SGP40 sensor initialized successfully.")
    print("Serial ID:", sensor.get_serial_id())
    
    try:
        while True:
            # Example humidity and temperature (replace with actual sensor values if available)
            humidity = 50.0
            temperature = 25.0

            try:
                raw, voc_index = sensor.measure_voc_index(humidity, temperature)
                print(f"Raw VOC: {raw:,} → VOC Index:", voc_index)
            except SGP40.CRCException:
                print("CRC error while reading sensor data!")

            utime.sleep(1.0)

    except KeyboardInterrupt:
        print("\nShutting down...")
