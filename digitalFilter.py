######################################################################################
# digitalFilter.py: Creates a digital low pass filter of roll and pitch
# set last roll and pitch value = alpha * previous value + (1-alpha) * newest reading
# alpha = 0.2 introduces small delay in response to changes in pitch or roll
# filtered roll, pitch values instead of directly filtering acc vectors
#
# digitalFilter.py is a low pass filter version of tilt.py:
# tilt.py reads data from BNO055 via serial port and plots roll and pitch in
# degrees in real time plot.  It reads the serial port as formatted by main.cpp.
# calculated: roll, degrees = atan2(acc_y, acc_z)* 180/pi
#             pitch,degrees = atan2(acc_x,acc_z) * 180/pi
# Warning:  note the commas required in the return statement of animate().
# Using matplotlib.animate.FuncAnimation() to plot live data. make sure blit=True in
# Funcanimation()
######################################################################################


import serial
import matplotlib.pyplot as plt
from matplotlib import animation
from time import sleep
import math

# xs and roll_array, pitch_array =last 50 roll values for live data chart
xs = [i for i in range(50)]   # x axis for chart.  Latest 50 values
roll_array = [0]*50   # last 50 roll values
pitch_array = [0]*50  # last 50 pitch values

# digital filter on acc vectors
# alpha:  (1-alpha) * new data vector + alpha * last stored data vector
alpha = .8  # data appended is combination of new and previous value

# get a figure and axis for data
fig, ax = plt.subplots(1, 2)  # roll, pitch in separate subplots

# empty lines to be updated by animate()
line_roll, = ax[0].plot(xs, roll_array, 'bo-',
                        label="roll")  # roll data to plot
line_pitch, = ax[1].plot(xs, pitch_array, 'ro-', label="pitch")  # pitch data

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
    # the  roll_array, pitch_array arrays holding the roll, pitch data
    while serialPort.inWaiting == 0:
        pass
    try:
        dataString = serialPort.readline().decode('utf-8')
        data = dataString.split(',')
        for i in range(len(data)):
            data[i] = float(data[i])

        a_x = data[0]
        a_y = data[1]
        a_z = data[2]
        roll = calcRoll(a_y, a_z)
        # new roll value =  (1-alpha)% new value + alpha% last value
        roll = (1-alpha) * roll + alpha * roll_array[-1]
        roll_array.append(roll)
        roll_array.pop(0)
        pitch = calcPitch(a_x, a_z)
        # new pitch value =  (1-alpha)% new value + alpha% last value
        pitch = (1-alpha)*pitch + alpha * pitch_array[-1]
        pitch_array.append(pitch)
        pitch_array.pop(0)
    except:
        pass
    return


def animate(i):
    # global roll_array  # to update roll array
    # global line_roll
    getSerialData(serialPort)
    line_roll.set_data(xs, roll_array)  # latest roll data
    line_pitch.set_data(xs, pitch_array)  # latest pitch data

    # NOTE THE TRAILING COMMA, VERY IMPORTANT: iterator!!!!
    return line_roll, line_pitch,


serialPort = serial.Serial("COM3", 115200)
sleep(.1)
serialPort.flushInput()
anim = animation.FuncAnimation(
    fig, animate, interval=20, save_count=10, cache_frame_data=True, blit=True)

plt.suptitle("Low Pass Filter Acc Vectors")
plt.show()
