import pycxsimulator
from pylab import *
import pandas as pd
import numpy as np
import random
from enum import Enum
from matplotlib import colors
from Person import Person
from PersonState import PersonState

n = 100 # size of space: n x n
p = 0.1 # probability of initially panicky individuals

maxState = 5



def initialize():
    global todayPersons, nextDayPersons, foo, nextfoo

    todayPersons = np.full((n, n), Person())
    foo = np.full((n, n), 0)
    for i, persons in enumerate(todayPersons):
        for j, person in enumerate(persons):
            person.set_values()
            foo[i,j] = person.state.value
    nextDayPersons = np.full((n, n), Person())
    nextfoo = np.full((n, n), 0)


def observe():
    global todayPersons, nextDayPersons, foo
    cla()
    cmap = colors.ListedColormap(['w','b','y','g','r','k'])
    print(foo)
    imshow(foo, vmin = 0, vmax = 5, cmap=cmap)


def update():
    global todayPersons, nextDayPersons, foo, nextfoo
    for x in range(n):
        for y in range(n):
            state = todayPersons[x][y].state.value
            if state == PersonState.DEATH:
                continue
            if state == PersonState.HEALTHY:
                num = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if todayPersons[(y + dy) % n][(x + dx) % n].state.value == PersonState.INFECTIOUS:
                            num += 1
                if random.uniform(0, 1) * 3 < num:
                    state = PersonState.INFECTIOUS
                else:
                    state = PersonState.HEALTHY
            else:
                state += 1
            nextDayPersons[x][y].state = PersonState(state)
            #PersonState(1) if count >= 4 else PersonState(0)
            nextfoo[x][y] = nextDayPersons[x][y].state.value
    todayPersons, nextDayPersons = nextDayPersons, todayPersons
    foo, nextfoo = nextfoo, foo


pycxsimulator.GUI().start(func=[initialize, observe, update])
