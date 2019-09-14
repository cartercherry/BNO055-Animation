####################################################
# 9/6/19  This plots all data streams in 4 subplots!!!!!
# read serial BNO055 data using numpy arrays
# cannot use append!
# incorporate with animation
##################################################

import serial
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import matplotlib.animation as animation

# open serial port for data stream reading
BNO055Data = serial.Serial('COM3', 115200)  # data from sensor on com3
sleep(0.1)
BNO055Data.flushInput()

count = 0  # index into data array streams, 0-50

# initialize data array streams with all zeros
acc_x = np.zeros([50], dtype=np.float32)
acc_y = np.zeros([50], dtype=np.float32)
acc_z = np.zeros([50], dtype=np.float32)

gyro_x = np.zeros([50], dtype=np.float32)
gyro_y = np.zeros([50], dtype=np.float32)
gyro_z = np.zeros([50], dtype=np.float32)

mag_x = np.zeros([50], dtype=np.float32)
mag_y = np.zeros([50], dtype=np.float32)
mag_z = np.zeros([50], dtype=np.float32)

quat_w = np.zeros([50], dtype=np.float32)
quat_x = np.zeros([50], dtype=np.float32)
quat_y = np.zeros([50], dtype=np.float32)
quat_z = np.zeros([50], dtype=np.float32)


fig, ax = plt.subplots(2, 2)  # four subplots in a 2X2 grid

# data arrays hold the last 50 data points from each data stream; "x axis"
x = np.arange(0, 50, 1)

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


ax[0, 0].set_ylim((-11, 11))  # accelerometer
ax[0, 0].set_ylabel('acc m/s^2')
ax[0, 0].set_title('Accelerometer')
ax[0, 0].legend(loc='lower center')
ax[0, 1].set_ylim((-300, 300))  # gyrometer
ax[0, 1].set_title('Gyrometer')
ax[0, 1].legend(loc='best')
ax[1, 0].set_ylim((-50, 50))  # magnetometer
ax[1, 0].set_title("Magnetometer")
ax[1, 0].legend(loc='best')
ax[1, 1].set_ylim((-1.1, 1.1))  # quaternion
ax[1, 1].set_title("Quaternions (w,x,y,z)")
ax[1, 1].legend(loc='lower center')
ax[0, 0].grid(True)
ax[0, 1].grid(True)
ax[1, 0].grid(True)
ax[1, 1].grid(True)

plt.style.use('seaborn')  # fivethirtyeight
plt.tight_layout()
#fig.legend(loc='lower center')
plt.suptitle('BNO055 Live Data')
# fig.show()


def updateDataArrays():
    global count, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, quat_w, quat_x, quat_y, quat_z

    while BNO055Data.inWaiting() == 0:
        pass
    try:
        data_string = BNO055Data.readline().decode(
            'utf-8')  # convert bytestring to utf-8

    except:
        pass
    data_array = data_string.split(',')
    for i in range(len(data_array)):
        try:
            data_array[i] = float(data_array[i])  # string to float data
        except:
            data_array[i] = 0  # data_array[max(0, i-1)]

    try:

        acc_x[count % 50] = data_array[0]
        acc_y[count % 50] = data_array[1]
        acc_z[count % 50] = data_array[2]
        gyro_x[count % 50] = data_array[3]
        gyro_y[count % 50] = data_array[4]
        gyro_z[count % 50] = data_array[5]
        mag_x[count % 50] = data_array[6]
        mag_y[count % 50] = data_array[7]
        mag_z[count % 50] = data_array[8]
        quat_w[count % 50] = data_array[9]
        quat_x[count % 50] = data_array[10]
        quat_y[count % 50] = data_array[11]
        quat_z[count % 50] = data_array[12]
        count += 1
    except:
        print('error loading acc,gyro')
        pass


def animate(i):

    # print(f'i,x,x+i: {i} {x} {(x+i)%50}\n')  # DEBUG

    updateDataArrays()
    # update the data. DEBUG!!  all were x+1, not x
    linex.set_ydata(acc_x)  # DEBUG was (x)%50
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

    return linex, liney, linez, linexg, lineyg, linezg, linexm, lineym, linezm, linewq, linexq, lineyq, linezq


ani = animation.FuncAnimation(
    fig, animate, interval=2, blit=True, save_count=20, cache_frame_data=True)  # DEBUG was 10

plt.show()
