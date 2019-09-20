#################################################################
# live matplotlib plot of magnetic heading +/- 180 degrees
# heading, degrees = np.arctan2(mag_y,mag_x) * 180/np.pi
# mag_x = data_array[6]   mag_y = data_array[7]  from serial port
# BNO055 serial port data on COM3 baudrate 115200 by main.ccp
# matplotlib.animation.Funcanimation  blit=True
#################################################################

import serial
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from time import sleep


# arrays to hold degrees and fixed arrow length of polar plot
degrees_array = [0]*50  # holds last 50 degree data from BNO055
# arrow_array = [1]*50  # length of arrow on polar plot


def getSerialData(serialPort):
    while serialPort.inWaiting == 0:
        pass
    try:
        data_array = serialPort.readline().decode('utf-8')
        data = data_array.split(',')
        mag_x = float(data[6])
        mag_y = float(data[7])
        #mag_z = float(data[8])
        # print(data)
        # DEBUG
        #print(f'mag_x: {mag_x:.2f}, mag_y: {mag_y:.2f}, mag_z: {mag_z:.2f}')
    except:
        print('error in getSerialData')
        pass
    return mag_x, mag_y


def getHeading(mag_x, mag_y):
    degrees = np.arctan2(mag_y, mag_x) * 180/np.pi
    if degrees > 0:
        degrees -= 180
    else:
        degrees += 180
    degrees_array.pop(0)  # update degrees_array with latest heading
    degrees_array.append(degrees)
    return degrees


def animate(i):
    mag_x, mag_y = getSerialData(bno)
    degrees = getHeading(mag_x, mag_y)
    degrees_array.append(degrees)
    degrees_array.pop(0)
    lineM.set_ydata(degrees_array)
    return lineM,


bno = serial.Serial("COM3", 115200)
sleep(.1)
bno.flushInput()
xs = [i for i in range(50)]  # x axis values, last 50
fig, ax = plt.subplots()
# magnetic heading line array
lineM, = ax.plot(xs, degrees_array, 'ro-')
ax.set_ylim((-190, 190))
ax.set_ylabel('\u03bcT')  # unicode micro symbol
ax.set_xlabel('t')
ax.set_title('Magnetic Heading')
ax.legend(loc='best')
ax.grid(True)
ax.set_facecolor('beige')

ani = animation.FuncAnimation(
    fig, animate, interval=10, blit=True, save_count=10, cache_frame_data=True)
plt.show()
