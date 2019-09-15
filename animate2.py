#########################################################################################################
# animate2.py reads BNO055 data on COM3, 115200 and plots live data into 4 subplots
# platformIO/Projects/BNO055/main.cpp reads data into COM3
# update 9/14/19  runs at 9 frames/sec in 4 subplots - push from VS code
# using list append/pop methods and funcAnimation()  blit=True
# No numpy arrays - didn't really increase frame rate
#
# received data_array[] format:
# 0       1       2       3       4       5       6       7       8     9        10      11      12
# acc_x   acc_y   acc_z   gyro_x  gyro_y  gyro_z  mag_x   mag_y   mag_z quat_w    quat_x  quat_y  quat_z
#########################################################################################################

import serial
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import matplotlib.animation as animation
import time

# open serial port for data stream reading
BNO055Data = serial.Serial('COM3', 115200)  # data from sensor on COM3
sleep(0.1)
BNO055Data.flushInput()  # get rid of old data in serial buffer


# initialize data arrays with all zeros
# looking at last 50 data points on each stream
acc_x = [0]*50
acc_y = [0]*50
acc_z = [0]*50

gyro_x = [0]*50
gyro_y = [0]*50
gyro_z = [0]*50

mag_x = [0]*50
mag_y = [0]*50
mag_z = [0]*50

quat_w = [0]*50
quat_x = [0]*50
quat_y = [0]*50
quat_z = [0]*50


fig, ax = plt.subplots(2, 2)  # figure, Axes;  four subplots  2 row X 2 col


x = [i for i in range(50)]  # x axis for data plots

# setup lines to hold data for each stream
# these will be updated by animate()
linex, = ax[0, 0].plot(x, acc_x, label='acc_x')
liney, = ax[0, 0].plot(x, acc_y, label='acc_y')
linez, = ax[0, 0].plot(x, acc_z, label='acc_z')
linexg, = ax[0, 1].plot(x, gyro_x, label='gyro_x')
lineyg, = ax[0, 1].plot(x, gyro_y, label='gyro_y')
linezg, = ax[0, 1].plot(x, gyro_z, label='gyro_z')
linexm, = ax[1, 0].plot(x, mag_x, label='mag_x')
lineym, = ax[1, 0].plot(x, mag_y, label='mag_y')
linezm, = ax[1, 0].plot(x, mag_z, label='mag_z')
linewq, = ax[1, 1].plot(x, quat_w, label='quat_w')
linexq, = ax[1, 1].plot(x, quat_x, label='quat_x')
lineyq, = ax[1, 1].plot(x, quat_y, label='quat_y')
linezq, = ax[1, 1].plot(x, quat_z, label='quat_z')

# set misc. Axis properties for each stream/subplot
ax[0, 0].set_ylim((-11, 11))  # accelerometer
ax[0, 0].set_ylabel('acc m/s^2')
ax[0, 0].set_title('Accelerometer')
ax[0, 0].legend(loc='lower center')
ax[0, 1].set_ylim((-300, 300))  # gyrometer
ax[0, 1].set_ylabel('radians/s')
ax[0, 1].set_title('Gyrometer')
ax[0, 1].legend(loc='best')
ax[1, 0].set_ylim((-50, 50))  # magnetometer
ax[1, 0].set_ylabel('\u03bcT')  # mu in unicode
ax[1, 0].set_title("Magnetometer")
ax[1, 0].legend(loc='best')
ax[1, 1].set_ylim((-1.1, 1.1))  # quaternion
ax[1, 1].set_title("Quaternions (w,x,y,z)")
ax[1, 1].legend(loc='lower center')
ax[0, 0].grid(True)  # grids are nice
ax[0, 1].grid(True)
ax[1, 0].grid(True)
ax[1, 1].grid(True)

# plt.style.use('seaborn')  # fivethirtyeight
# plt.tight_layout()
plt.suptitle('BNO055 Live Data')


def getData():
    while BNO055Data.inWaiting() == 0:
        pass
    try:
        data_string = BNO055Data.readline().decode(
            'utf-8')  # bytestring to utf-8

    except:
        print('data_string error')
    data_array = data_string.split(',')
    for i in range(len(data_array)):
        try:
            data_array[i] = float(data_array[i])  # string to float data
        except:
            data_array[i] = 0  # if error, put 0 in array
            print('data_array error')
    return data_array


def animate(i):
    # time each animate invocation
    #start = time.perf_counter()

    global acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, quat_w, quat_x, quat_y, quat_z

    data_array = getData()
    acc_x.append(data_array[0])
    acc_x.pop(0)
    acc_y.append(data_array[1])
    acc_y.pop(0)  # acc_y = acc_y[1:]  seems no different that acc_y.pop(0)
    acc_z.append(data_array[2])
    acc_z.pop(0)
    gyro_x.append(data_array[3])
    gyro_x.pop(0)
    gyro_y.append(data_array[4])
    gyro_y.pop(0)
    gyro_z.append(data_array[5])
    gyro_z.pop(0)
    mag_x.append(data_array[6])
    mag_x.pop(0)
    mag_y.append(data_array[7])
    mag_y.pop(0)
    mag_z.append(data_array[8])
    mag_z.pop(0)
    quat_w.append(data_array[9])
    quat_w.pop(0)
    quat_x.append(data_array[10])
    quat_x.pop(0)
    quat_y.append(data_array[11])
    quat_y.pop(0)
    quat_z.append(data_array[12])
    quat_z.pop(0)

    # update each line with latest data for animation
    linex.set_ydata(acc_x)
    liney.set_ydata(acc_y)
    linez.set_ydata(acc_z)
    linexg.set_ydata(gyro_x)
    lineyg.set_ydata(gyro_y)
    linezg.set_ydata(gyro_z)
    linexm.set_ydata(mag_x)
    lineym.set_ydata(mag_y)
    linezm.set_ydata(mag_z)
    linewq.set_ydata(quat_w)
    linexq.set_ydata(quat_x)
    lineyq.set_ydata(quat_y)
    linezq.set_ydata(quat_z)

    #stop = time.perf_counter()
    print(f'{(stop-start)*1000:.2f}ms')
    return linex, liney, linez, linexg, lineyg, linezg, linexm, lineym, linezm, linewq, linexq, lineyq, linezq


ani = animation.FuncAnimation(
    fig, animate, interval=10, blit=True, save_count=10, cache_frame_data=True)  # blit=True vry important!

plt.show()
