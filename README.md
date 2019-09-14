# BNO055-Animation     cartercherry&pi;
BNO055 9 dof sensor. 
Plotting live data with matplotlib.animation.funcAnimation.  
Runs at 9 frames/sec

main.cpp can be renamed to run in an arduino ide instead of platformIO with esp32 as I am doing.  
main.cpp transmits the 3 acc, 3 gyro, 3 mag, and 4 quat streams via serial port 115200 baud

animate2.py uses matplotlib.animation.FuncAnimation to plt the live data coming from
the serial port.  All data in one figure with 4 subplots (two rows by two columns).  Very
important that the blit=True option set in FuncAnimation().
Noticed no difference in speed whether numpy arrays were used, so  using python
lists, append(), and pop()

These are my personal notes.  Thanks to Paul McWhorter for inspiration to plot live data.  

