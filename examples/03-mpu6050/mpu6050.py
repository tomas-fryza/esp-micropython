import time
import math

# Device addresses
MPU6050_ADDR = 0x68

# MPU6050 addresses
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
TEMP_OUT_H = 0x41
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
POWER_MGMT_1 = 0x6B

# Accel limit | Sensitivity
# 2g          | 16_384
# 4g          | 8_192
# 8g          | 4_096
# 16g         | 2_048

# Angular velocity limit | Sensitivity
# 250deg/s               | 131
# 500deg/s               | 65.5
# 1000deg/s              | 32.8
# 2000deg/s              | 16.4

# Sensitivity scales
ACCEL_SCALE = 16384.0  # Accelerometer scale for ±2g (16-bit)
GYRO_SCALE = 131.0  # Gyroscope scale for ±250°/s (16-bit)

# Other
RAD_TO_DEG = 180.0 / math.pi


class MPU6050:
    def __init__(self, i2c, address=MPU6050_ADDR):
        self.address = address
        self.i2c = i2c
        self.accel_offset_x = 0
        self.accel_offset_y = 0
        self.accel_offset_z = 0
        self.gyro_offset_x = 0
        self.gyro_offset_y = 0
        self.gyro_offset_z = 0
        self.yaw = 0
        self.last_time = time.ticks_ms()
        self._init_mpu6050()

    def _init_mpu6050(self):
        # Wake up, enable temperature sensor, internal 8MHz oscillator
        self.i2c.writeto(self.address, bytearray([POWER_MGMT_1, 0]))
        
        # TODO: Setup resolution and filters

    def _get_raw(self, addr):
        # Accel_X_H:L
        # Accel_Y_H:L
        # Accel_Z_H:L
        # Temp_H:L
        # Gyro_X_H:L
        # Gyro_Y_H:L
        # Gyro_Z_H:L
        high, low = self.i2c.readfrom_mem(self.address, addr, 2)
        time.sleep_ms(2)

        if not high & 0x80:
            return high << 8 | low
        return - (((high ^ 255) << 8) | (low ^ 255) + 1)

    def get_values(self):
        ax = self._get_raw(ACCEL_XOUT_H)
        ay = self._get_raw(ACCEL_YOUT_H)
        az = self._get_raw(ACCEL_ZOUT_H)
        temp = self._get_raw(TEMP_OUT_H)
        gx = self._get_raw(GYRO_XOUT_H)
        gy = self._get_raw(GYRO_YOUT_H)
        gz = self._get_raw(GYRO_ZOUT_H)

        # Convert to 'g' (gravity)
        ax = ax / ACCEL_SCALE - self.accel_offset_x
        ay = ay / ACCEL_SCALE - self.accel_offset_y
        az = az / ACCEL_SCALE - self.accel_offset_z

        # Temperature_in_celsius = raw_temperature / 340.0 + 36.53
        temp = temp / 340.0 + 36.53

        # Convert to degrees per second
        gx = gx / GYRO_SCALE - self.gyro_offset_x
        gy = gy / GYRO_SCALE - self.gyro_offset_y
        gz = gz / GYRO_SCALE - self.gyro_offset_z

        return ax, ay, az, temp, gz, gy, gz

    def calibrate(self):
        # Calibrate the sensor by averaging several readings for both accelerometer and gyroscope
        print("Calibrating MPU6050, hold still... ", end="")
        time.sleep_ms(500)

        # Discard first 100 measures
        for _ in range(100):
            ax, ay, az, temp, gx, gy, gz = self.get_values()
            time.sleep_ms(2)

        n_samples = 100
        for _ in range(n_samples):
            ax, ay, az, temp, gx, gy, gz = self.get_values()
            self.accel_offset_x += ax
            self.accel_offset_y += ay
            self.accel_offset_z += az
            self.gyro_offset_x += gx
            self.gyro_offset_y += gy
            self.gyro_offset_z += gz
            time.sleep_ms(2)

        self.accel_offset_x /= n_samples
        self.accel_offset_y /= n_samples
        self.accel_offset_z /= n_samples
        self.gyro_offset_x /= n_samples
        self.gyro_offset_y /= n_samples
        self.gyro_offset_z /= n_samples

        # Adjust for gravity on the Z-axis
        self.accel_offset_z -= 1.0;

        print("Done")

    def calculate_orientation(self):
        ax, ay, az, temp, gx, gy, gz = self.get_values()

        # Calculate pitch and roll from accelerometer data
        # https://engineering.stackexchange.com/questions/3348/calculating-pitch-yaw-and-roll-from-mag-acc-and-gyro-data
        pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * RAD_TO_DEG
        roll = math.atan2(ay, az) * RAD_TO_DEG

        # Time difference in seconds
        current_time = time.ticks_ms()
        dt = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

        # Calculate yaw from gyroscope data (simple integration)
        self.yaw += gz * dt

        # Pitch: The angle between local level and the longitudinal
        # axis of the aircraft. It is defined as positive for the nose
        # of the aircraft pointing above local level.
        #
        # Roll: The angle of rotation about the longitudinal axis of
        # the aircraft. Roll is defined as 0° when the aircraft is
        # upright and the lateral axis is in the level plane. It is
        # defined as positive for the right wing of the aircraft below
        # the left wing.
        #
        # Heading: The relative angle between the projection of the
        # longitudinal axis of the aircraft onto the local level frame
        # and some definition of North, for example either True North
        # or Magnetic North. Heading is positive for angles clockwise
        # from (east of) North.
        return -pitch, -roll, -self.yaw
