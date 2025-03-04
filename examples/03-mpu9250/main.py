# MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver
# https://github.com/tuupola/micropython-mpu9250

# Kalman filter
# https://github.com/micropython-IMU/micropython-fusion?tab=readme-ov-file
# Kalman for Arduino
# https://how2electronics.com/measure-pitch-roll-yaw-with-mpu6050-hmc5883l-esp32/
# https://github.com/nhatuan84/Arduino-KalmanFilter/tree/main
# Kalman for ESP-IDF
# https://github.com/JChunX/imu-kalman/tree/main


import utime
from machine import SoftI2C, Pin
import math

from mpu9250 import MPU9250
# from mpu6500 import MPU6500, SF_G, SF_DEG_S
from ak8963 import AK8963

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
print(f"I2C configuration: {str(i2c)}")

# mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
# sensor = MPU9250(i2c, mpu6500=mpu6500)
dummy = MPU9250(i2c) # this opens the bybass to access to the AK8963
ak8963 = AK8963(
    i2c,
    offset=(-7.423243, 18.58711, -124.3011),
    scale=(1.113371, 0.9323783, 0.971533))
# offset, scale = ak8963.calibrate(count=256, delay=200)
# print(offset, scale)

sensor = MPU9250(i2c, ak8963=ak8963)

# print("MPU9250 id: " + hex(sensor.whoami))
print("\nPress `Ctrl+C` to stop\n")

try:
    while True:
        ax, ay, az = sensor.acceleration
        gx, gy, gz = sensor.gyro
        mx, my, mz = sensor.magnetic
        temp = sensor.temperature

        # Calculate pitch and roll from accelerometer data
        # https://engineering.stackexchange.com/questions/3348/calculating-pitch-yaw-and-roll-from-mag-acc-and-gyro-data
        pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180.0 / math.pi
        roll = math.atan2(ay, az) * 180.0 / math.pi

        yaw = math.atan2(my, mx)
        if yaw < 0:
            yaw += 2.0 * math.pi
        if yaw > 2.0 * math.pi:
            yaw -= 2 * math.pi
        yaw = yaw * 180.0 / math.pi

        print(f"{pitch:.1f} \t{roll:.1f} \t{yaw:.1f} \t{temp:.1f}")
        utime.sleep_ms(1000)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
