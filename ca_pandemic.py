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
    global todayPersons, nextDayPersons, state_visualization_matrix
    todayPersons = np.full((n, n), Person())
    state_visualization_matrix = np.full((n, n), 0)
    for i, persons in enumerate(todayPersons):
        for j, person in enumerate(persons):
            person.set_values()
            state_visualization_matrix[i,j] = person.state.value
    nextDayPersons = np.full((n, n), Person())


def observe():
    global todayPersons, nextDayPersons, state_visualization_matrix
    cla()
    cmap = colors.ListedColormap(['w','b','y','g','r','k'])
    print(state_visualization_matrix)
    imshow(state_visualization_matrix, vmin = 0, vmax = 5, cmap=cmap)


def update():
    global todayPersons, nextDayPersons, state_visualization_matrix
    for x in range(n):
        for y in range(n):
            state = todayPersons[x][y].state.value
            if state == PersonState.DEATH.value:
                continue
            elif state == PersonState.HEALTHY.value:
                num = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if todayPersons[(y + dy) % n][(x + dx) % n].state.value == PersonState.INFECTIOUS.value:
                            num += 1
                if num > 2:
                    state = PersonState.INFECTIOUS.value
                else:
                    state = PersonState.HEALTHY.value
            else:
                state += 1
            nextDayPersons[x][y].state = PersonState(state)
            #PersonState(1) if count >= 4 else PersonState(0)
            state_visualization_matrix[x][y] = nextDayPersons[x][y].state.value
    todayPersons, nextDayPersons = nextDayPersons, todayPersons
pycxsimulator.GUI().start(func=[initialize, observe, update])
