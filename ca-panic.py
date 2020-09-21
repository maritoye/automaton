import pycxsimulator
from pylab import *
import numpy as np

n = 1000  # size of space: n x n
p = 0.24  # probability of initially panicky individuals


class Person:
    pass


def initialize():
    global todayPersons, nextDayPersons
    todayPersons = np.full((n, n), Person)

    for x in range(n):
        for y in range(n):

            todayPersons[x, y] = 1 if random() < p else 0

    np.full((n, n), Person)


def observe():
    global todayPersons, nextDayPersons
    cla()
    imshow(todayPersons, vmin=0, vmax=1, cmap=cm.binary)


def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n]
            nextconfig[x, y] = 1 if count >= 4 else 0
    config, nextconfig = nextconfig, config


pycxsimulator.GUI().start(func=[initialize, observe, update])
