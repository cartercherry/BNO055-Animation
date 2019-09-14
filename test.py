import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
fig.set_tight_layout(True)

x = np.arange(0, 20, 0.1)
line, = ax.plot(x, x - 5, 'r-', linewidth=2)

ax.plot(x, x, 'b', linewidth=2)


def update(i):
    label = 'timestep {0}'.format(i)
    line.set_ydata(0 + x*i)
    ax.set_xlabel(label)
    return line, ax


if __name__ == '__main__':
    anim = FuncAnimation(
        fig, update, frames=np.arange(0, 10, 0.1), interval=200)
    plt.grid(True)
    plt.title("Matplotlib Animation")
    plt.show()
