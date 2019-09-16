######################################################################
# roll.py reads data from BNO055 via serial port and plots roll in
# degrees in real time plot.  It reads the serial port as formatted by main.cpp.  Roll is
# calculated: roll, degrees = atan2(acc_y, acc_z)* 180/pi
# Warning:  note the commas required in the return statement of animate().
# Using matplotlib.animate.FuncAnimation() to plot live data. make sure blit=True in
# Funcanimation()
######################################################################


import serial
import matplotlib.pyplot as plt
from matplotlib import animation
from time import sleep
import math

# xs and ys=last 50 roll values for live data chart
xs = [i for i in range(50)]   # x axis for chart.  Latest 50 values
ys = [0]*50   # the last 50 roll values

# get a figure and axis for data
fig, ax = plt.subplots(1, 1)  # single subplot ax=Axes
# empty line to be updated by animate()
line_roll, = ax.plot(xs, ys, 'bo-', label="roll")  # line data to plot
ax.set_ylim(-180, 180)  # -180 to 180 degrees roll
ax.set_ylabel('degrees roll')
ax.set_title('Degrees Roll')
ax.legend(loc='best')
ax.grid(True)
ax.set_facecolor('beige')
# print(dir(ax))  #axes properties available to change


def calcRoll(acc_y, acc_z):
    '''calculates roll angle in degrees: atan2(acc_y,acc_z)*180/pi'''

    roll_Degrees = math.atan2(acc_y, acc_z) * 180/math.pi
    return roll_Degrees


def getSerialData(serialPort):
    # gets the latest BNO055 data, calculates the roll, and updates
    # the  ys array holding the roll data
    while serialPort.inWaiting == 0:
        pass
    try:
        dataString = serialPort.readline().decode('utf-8')
        data = dataString.split(',')
        for i in range(len(data)):
            data[i] = float(data[i])
        acc_y = data[1]
        acc_z = data[2]
        roll = calcRoll(acc_y, acc_z)
        ys.append(roll)
        ys.pop(0)
        #print(ys)  # DEBUG######################
        # print(f'{roll:.2f} \u00b0')  # degrees unicode  #DEBUG
    except:
        pass
    return


def animate(i):
    # global ys  # to update roll array
    # global line_roll
    getSerialData(serialPort)

    line_roll.set_data(xs, ys)  # latest roll data

    return line_roll,  # NOTE THE TRAILING COMMA, VERY IMPORTANT: iterator!!!!


serialPort = serial.Serial("COM3", 115200)
sleep(.1)
serialPort.flushInput()
anim = animation.FuncAnimation(
    fig, animate, interval=20, save_count=10, cache_frame_data=True, blit=True)


plt.show()
