# BNO055-Animation
BNO055 9 dof sensor. 
Plotting live data with matplotlib.animation.funcAnimation
Runs at 9 frames/sec

main.cpp can be renamed to run in an arduino ide instead of platformIO as I am doing
main.cpp transmits the 3 acc, 3 gyro, 3 mag, and 4 quat streams via serial port

Noticed no difference in speed whether numpy arrays were used, so am using python
lists, append(), and pop()

These are my personal notes, and not intended for public critique.  

