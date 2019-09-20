######################################################################
# tiilt.py reads data from BNO055 via serial port and plots roll and pitch in
# degrees in real time plot.  It reads the serial port as formatted by main.cpp.
# calculated: roll, degrees = atan2(acc_y, acc_z)* 180/pi
#             pitch,degrees = atan2(acc_x,acc_z) * 180/pi
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
ys = [0]*50   # last 50 roll values
ys1 = [0]*50  # last 50 pitch values

# get a figure and axis for data
fig, ax = plt.subplots(1, 2)  # roll, pitch in separate subplots

# empty lines to be updated by animate()
line_roll, = ax[0].plot(xs, ys, 'bo-', label="roll")  # roll data to plot
line_pitch, = ax[1].plot(xs, ys1, 'ro-', label="pitch")  # pitch data

ax[0].set_ylim(-180, 180)  # -180 to 180 degrees roll
ax[0].set_ylabel('degrees roll')
ax[0].set_title('Degrees Roll')
ax[0].legend(loc='best')
ax[0].grid(True)
ax[0].set_facecolor('beige')

ax[1].set_ylim(-180, 180)  # -180 to 180 degrees roll
ax[1].set_ylabel('degrees pitch')
ax[1].set_title('Degrees Pitch')
ax[1].legend(loc='best')
ax[1].grid(True)
ax[1].set_facecolor('beige')


# print(dir(ax))  #axes properties available to change


def calcRoll(acc_y, acc_z):
    '''calculates roll angle in degrees: atan2(acc_y,acc_z)*180/pi'''

    roll_Degrees = - math.atan2(acc_y, acc_z) * \
        180/math.pi  # - to reverse roll on graph
    return roll_Degrees


def calcPitch(acc_x, acc_z):
    '''calculates pitch angle in degrees: atan2(acc_x,acc_z)*180/pi'''

    pitch_Degrees = - math.atan2(acc_x, acc_z) * \
        180/math.pi  # - to reverse pitch on graph
    return pitch_Degrees


def getSerialData(serialPort):
    # gets the latest BNO055 data, calculates the roll and pitch, and updates
    # the  ys, ys1 arrays holding the roll, pitch data
    while serialPort.inWaiting == 0:
        pass
    try:
        dataString = serialPort.readline().decode('utf-8')
        data = dataString.split(',')
        for i in range(len(data)):
            data[i] = float(data[i])
        acc_x = data[0]
        acc_y = data[1]
        acc_z = data[2]
        roll = calcRoll(acc_y, acc_z)
        ys.append(roll)
        ys.pop(0)
        pitch = calcPitch(acc_x, acc_z)
        ys1.append(pitch)
        ys1.pop(0)
    except:
        pass
    return


def animate(i):
    # global ys  # to update roll array
    # global line_roll
    getSerialData(serialPort)
    line_roll.set_data(xs, ys)  # latest roll data
    line_pitch.set_data(xs, ys1)  # latest pitch data

    # NOTE THE TRAILING COMMA, VERY IMPORTANT: iterator!!!!
    return line_roll, line_pitch,


serialPort = serial.Serial("COM3", 115200)
sleep(.1)
serialPort.flushInput()
anim = animation.FuncAnimation(
    fig, animate, interval=20, save_count=10, cache_frame_data=True, blit=True)


plt.show()
