# BNO055-Animation cartercherry&pi;

BNO055 9 dof sensor.
Plotting live data with matplotlib.animation.funcAnimation.  
All live plots run at ~9 frames/sec. The BNO055 is updating the serial port with new data
10 times/sec.

main.cpp can be renamed (e.g. serialData.ino) to run without modification with the arduino ide.
I used visual studio code with platformIO on an esp32 (instead of arduino nano).  
main.cpp transmits the 3 acc, 3 gyro, 3 mag, and 4 quat streams via serial port 115200 baud

animate2.py uses matplotlib.animation.FuncAnimation to plt the live data coming from
the serial port. All data in one figure with 4 subplots (two rows by two columns). Very
important that the blit=True option set in FuncAnimation().
Noticed no difference in speed whether numpy arrays were used, so using python
lists, append(), and pop().

tilt.py uses the BNO055 acc_x, acc_y and acc_z vectors to calculate roll and pitch using matplotlib
animation inreal time. Uses same technique as animate2.py.

tilt.py serial data format expected at 115200 baud:
0 1 2
acc_x acc_y acc_z
