from vpython import *
from time import *
import numpy as np
import math
import serial

ad = serial.Serial('/dev/ttyUSB0', 115200)
sleep(1)

scene.range = 5
toRad = 2 * np.pi / 360
toDeg = 1 / toRad
scene.forward = vector(-1, -1, -1)

scene.width = 600
scene.height = 600

xarrow = arrow(lenght=2, shaftwidth=.1, color=color.red, axis=vector(1, 0, 0))
yarrow = arrow(lenght=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(lenght=4, shaftwidth=.1, color=color.blue, axis=vector(0, 0, 1))

frontArrow = arrow(length=4, shaftwidth=.1, color=color.purple, axis=vector(1, 0, 0))
upArrow = arrow(length=1, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))
sideArrow = arrow(length=2, shaftwidth=.1, color=color.orange, axis=vector(0, 0, 1))

bBoard = box(length=6, width=2, height=.2, opacity=.8, pos=vector(0, 0, 0, ))
bn = box(length=1, width=.75, height=.1, pos=vector(-.5, .1 + .05, 0), color=color.blue)
nano = box(lenght=1.75, width=.6, height=.1, pos=vector(-2, .1 + .05, 0), color=color.green)
myObj = compound([bBoard, bn, nano])
while True:
    while (ad.inWaiting() == 0):
        pass
    dataPacket = ad.readline()
    dataPacket = str(dataPacket, 'utf-8')
    splitPacket = dataPacket.split(",")
    roll = float(splitPacket[0]) * toRad
    pitch = float(splitPacket[1]) * toRad
    yaw = float(splitPacket[2]) * toRad
    print("Roll=", roll * toDeg, " Pitch=", pitch * toDeg, "Yaw=", yaw * toDeg)
    rate(50)
    k = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
    y = vector(0, 1, 0)
    s = cross(k, y)
    v = cross(s, k)

    frontArrow.axis = k
    sideArrow.axis = s
    upArrow.axis = v
    myObj.axis = k
    myObj.up = v
    sideArrow.length = 2
    frontArrow.length = 4
    upArrow.length = 1
