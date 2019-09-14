import random
import matplotlib.pyplot as plt
from matplotlib import style


def createData():
    xs, ys = [], []
    for i in range(10):
        x = i
        y = random.randint(0, 10)
        xs.append(x)
        ys.append(y)
    return xs, ys


style.use('fivethirtyeight')
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)
plt.title('Random Data')
plt.xlabel('number')
plt.ylabel('random int')

x, y = createData()
ax1.set_ylim(0, 10)
ax1.plot(x, y, 'r-*')
plt.legend()
plt.tight_layout()

x, y = createData()
ax2.set_ylim(0, 10)
ax2.plot(x, y, 'g^--')
plt.show()
