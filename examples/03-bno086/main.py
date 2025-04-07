"""
TBD

Inspired by:
  * https://github.com/dobodu/BOSCH-BNO085-I2C-micropython-library/tree/main
"""

from machine import I2C, Pin
from utime import ticks_ms, sleep_ms
import math
from bno08x import *

I2C1_SDA = Pin(21)
I2C1_SCL = Pin(22)

i2c1 = I2C(0, scl=I2C1_SCL, sda=I2C1_SDA, freq=100_000, timeout=200_000 )

bno = BNO08X(i2c1, debug=False)
print("BNO08x I2C connection : Done")

bno.enable_feature(BNO_REPORT_ACCELEROMETER, 20)
bno.enable_feature(BNO_REPORT_MAGNETOMETER,20 )
bno.enable_feature(BNO_REPORT_GYROSCOPE,20 )
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, 10)
bno.set_quaternion_euler_vector(BNO_REPORT_GAME_ROTATION_VECTOR)

print("BNO08x sensors enabling : Done")

cpt = 0
timer_origin = ticks_ms()
average_delay = -1

print("Press `Ctrl+C` to stop")

try:
    while True:
        sleep_ms(50)
        cpt += 1
        # print("cpt", cpt)
#         accel_x, accel_y, accel_z = bno.acc
#         print("Acceleration\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s²".format(accel_x, accel_y, accel_z))
#         gyro_x, gyro_y, gyro_z = bno.gyro
#         print("Gyroscope\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\trads/s".format(gyro_x, gyro_y, gyro_z))
#         mag_x, mag_y, mag_z = bno.mag
#         print("Magnetometer\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tuT".format(mag_x, mag_y, mag_z))
#         quat_i, quat_j, quat_k, quat_real = bno.quaternion
#         print("Rot Vect Quat\tI: {:+.3f}\tJ: {:+.3f}\tK: {:+.3f}\tReal: {:+.3f}".format(quat_i, quat_j, quat_k, quat_real))
        R, T, P = bno.euler
        print("Euler Angle\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}".format(R, T, P))
#         print("===================================")
#         print("average delay times (ms) :", average_delay)
#         print("===================================")
#         timer = ticks_ms()
#         if cpt == 10 :
#             bno.tare
#         if cpt % 100 == 0:
#             average_delay = (timer - timer_origin) / cpt

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
