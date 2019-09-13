# calculate magnetic direction from magnetometer data
# Direction in degrees = atan2(yGaussData/xGaussData) * pi/2
# use atan2() function from python library

import math
import serial
from time import sleep
# x = -30.1875
# y = -6.0


def tilt(accY, accZ):
    degreesTilt = math.atan2(accY, accZ)*180/math.pi
    return degreesTilt


def calHeading(x, y):
    magHeading = math.atan2(y, x) * 180/math.pi + \
        180  # degrees magnetic heading
    return magHeading


data_array_floats = []  # holds the BNO055 data as floats
# open serial port com3, 115200
dataStream = serial.Serial("com3", 115200)
sleep(.1)
dataStream.flushInput()
# wait for data on serial port
while dataStream.inWaiting() == 0:
    pass

# get the data
for i in range(500):
    dataString = dataStream.readline().decode('utf-8')
    # print(dataString)
    data = dataString.split(',')
    # print(data)
    for i in range(len(data)):
        data[i] = float(data[i])

    # get magnetometer x and y data
    # x = data[6]
    # y = data[7]
    # print(f'{calHeading(x, y):.1f}\u00b0')  # \u00b0 is degree symbol
    acc_y = data[1]
    acc_z = data[2]
    print(f'{tilt(acc_y,acc_z):.1f}\u00b0')


dataStream.close()
