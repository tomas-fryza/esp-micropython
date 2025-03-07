import time
import serial

esp_data=serial.Serial('/dev/ttyUSB0',115200)
time.sleep(1)
while True:
    while (esp_data.inWaiting()==0):
        pass

    dataPacket = esp_data.readline()
    dataPacket=str(dataPacket,'utf-8')
    splitPacket=dataPacket.split(",")
    roll=float(splitPacket[0])
    pitch=float(splitPacket[1])
    yaw=float(splitPacket[2])
    print(f"R={roll}, P={pitch}, Y={yaw}")
