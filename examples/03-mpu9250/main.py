# MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver:
# https://github.com/tuupola/micropython-mpu9250

# Arduino + IMU + VPython:
# https://toptechboy.com/arduino-based-9-axis-inertial-measurement-unit-imu-based-on-bno055-sensor/

# Kalman filter:
# https://how2electronics.com/measure-pitch-roll-yaw-with-mpu6050-hmc5883l-esp32/
# https://github.com/micropython-IMU/micropython-fusion?tab=readme-ov-file
# https://github.com/nhatuan84/Arduino-KalmanFilter/tree/main
# https://github.com/JChunX/imu-kalman/tree/main


import utime
from machine import SoftI2C, Pin
import math
from mpu9250 import MPU9250
# from mpu6500 import MPU6500, SF_G, SF_DEG_S
from ak8963 import AK8963

# Adjust yaw using magnetic declination angle
# https://www.magnetic-declination.com/
# +5°22' for Brno
magnetic_declination = 0.094  # rad = pi * (d+m/60) / 180

# --- KALMAN FILTER PARAMETERS ---
Q_angle = 0.001   # Process noise variance for the accelerometer
Q_bias = 0.003    # Process noise variance for the gyroscope bias
R_measure = 0.03  # Measurement noise variance
angle = 0  # Kalman filter state variables
bias = 0
rate = 0
P = [[0, 0], [0, 0]]  # Error covariance matrix
pitch, roll, yaw = 0, 0, 0


# Kalman filter function
def Kalman_filter(angle, gyroRate, accelAngle):
    global bias, P, dt, Q_angle, Q_bias, R_measure
    
    # Predict
    rate = gyroRate - bias
    angle += dt * rate
    
    # Update the error covariance matrix
    P[0][0] += dt * (dt * P[1][1] - P[0][1] - P[1][0] + Q_angle)
    P[0][1] -= dt * P[1][1]
    P[1][0] -= dt * P[1][1]
    P[1][1] += Q_bias * dt
    
    # Update
    S = P[0][0] + R_measure  # Estimate error
    K = [P[0][0] / S, P[1][0] / S]  # Kalman gain
    
    y = accelAngle - angle  # Angle difference
    angle += K[0] * y
    bias += K[1] * y
    
    # Update the error covariance matrix
    P00_temp = P[0][0]
    P01_temp = P[0][1]
    
    P[0][0] -= K[0] * P00_temp
    P[0][1] -= K[0] * P01_temp
    P[1][0] -= K[1] * P00_temp
    P[1][1] -= K[1] * P01_temp
    
    return angle


toRad = 2.0*math.pi / 360
toDeg = 1 / toRad

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
print(f"I2C configuration: {str(i2c)}")

# mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
# sensor = MPU9250(i2c, mpu6500=mpu6500)
dummy = MPU9250(i2c) # this opens the bybass to access to the AK8963
ak8963 = AK8963(i2c,
    offset=(47.79844, 46.37666, 66.57422),
    scale=(1.060139, 0.9904738, 0.9550097))
# ak8963 = AK8963(i2c)
# print("Calibrating! Rotate the sensor in all directions... ", end="")
# offset, scale = ak8963.calibrate(count=256, delay=200)
# print("Done")
# print(f"offset=({offset}), scale=({scale})")

sensor = MPU9250(i2c, ak8963=ak8963)

# Set the initial time for the loop
lastTime = utime.ticks_ms()

print("MPU9250 id: " + hex(sensor.whoami))
print("\nPress `Ctrl+C` to stop\n")

try:
    while True:
        ax, ay, az = sensor.acceleration
        gx, gy, gz = sensor.gyro
        mx, my, mz = sensor.magnetic
        temp = sensor.temperature

        # --- CALCULATE TIME STEP ---
        currentTime = utime.ticks_ms()
        dt = (currentTime - lastTime) / 1000.0  # Calculate time in seconds
        if (dt == 0):
            dt = 0.001  # Prevent division by zero
        lastTime = currentTime

        # Calculate pitch and roll from accelerometer data
        # https://engineering.stackexchange.com/questions/3348/calculating-pitch-yaw-and-roll-from-mag-acc-and-gyro-data
        # pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * toDeg
        # roll = math.atan2(ay, az) * toDeg

        # --- KALMAN FILTER FOR PITCH AND ROLL ---
        pitch = Kalman_filter(pitch, gx, math.atan2(-ax, math.sqrt(ay**2 + az**2)) * toDeg)
        roll = Kalman_filter(roll, gy, math.atan2(ay, az) * toDeg)

        # Calculate and adjust yaw from magnetometer data
        yaw = math.atan2(my, mx)
        yaw += magnetic_declination
        # Normalize yaw to 0--360 degrees
        if yaw < 0:
            yaw += 2.0 * math.pi
        if yaw > 2.0 * math.pi:
            yaw -= 2 * math.pi
        yaw = yaw * toDeg

        # print(f"{roll:.1f},{pitch:.1f},{yaw:.1f},{temp:.1f}")
        print(f"{roll:.1f},{pitch:.1f},{yaw:.1f}")
        utime.sleep_ms(20)  # 50 Hz

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
