# https://microcontrollerslab.com/micropython-mpu-6050-esp32-esp8266/
# https://how2electronics.com/measure-pitch-roll-yaw-with-mpu6050-hmc5883l-esp32/
# https://howtomechatronics.com/tutorials/arduino/arduino-and-mpu6050-accelerometer-and-gyroscope-tutorial/
# https://how2electronics.com/interfacing-mpu6050-accelerometer-gyroscope-with-arduino/

# The MPU6050 Explained
# https://mjwhite8119.github.io/Robots/mpu6050

from machine import Pin, I2C
import time
import mpu6050

led = Pin(2, Pin.OUT)

# Connect the MPU6050 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #, freq=100_000)
print(f"I2C configuration: {str(i2c)}")

mpu = mpu6050.MPU6050(i2c)
led.on()
mpu.calibrate()
led.off()

print("\nPress `Ctrl+C` to stop\n")
# print("roll;pitch;yaw")

try:
    while True:
        # pitch, roll, yaw = mpu.calculate_orientation()
        # Different module orientation
        roll, pitch, yaw = mpu.calculate_orientation()
        print(f"Roll: {roll:.1f}°\tPitch: {pitch:.1f}°\tYaw(Z): {yaw:.1f}°")
        time.sleep_ms(200)

except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("\nProgram stopped. Exiting...")

    # Optional cleanup code
    led.off()
