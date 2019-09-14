import matplotlib.pyplot as plt
import numpy as np
import math


def cart2polar(x, y):  # convert x,y to r,theta
    theta = np.arctan2(y, x)
    r = np.hypot(x, y)  # hypotenuse
    return theta, r


def compass(u, v, arrowprops=None):
    '''compass draws a graph that displays the
    vectors with components 'u,'v' as arrows from
    the origin'''

    angles, radii = cart2polar(u, v)

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    kw = dict(arrowstyle='->', color='b')
    arrowprops = dict(color='darkorange', linewidth=4)
    if arrowprops:
        kw.update(arrowprops)
    [ax.annotate("", xy=(angle, radius), xytext=(0, 0),
                 arrowprops=kw) for angle, radius in zip(angles, radii)]
    ax.set_ylim(0, np.max(radii))
    ax.set_title('Tilt Angle', pad=8)  # pad separates title from graph
    return fig, ax


u = [9.73]  # acc_z
v = [0.24]  # acc_y
fig, ax = compass(u, v)
plt.show()


# x = -1
# y = 0
# r, theta = cart2polar(x, y)
# # degrees = \u00b0
# print(f'x:{x}, y:{y} => r:{r:.2f}, theta:{theta:.2f}\u00b0')
