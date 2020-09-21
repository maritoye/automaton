import pycxsimulator
from pylab import *
import pandas as pd
import numpy as np
import random
from enum import Enum

n = 100 # size of space: n x n
p = 0.24 # probability of initially panicky individuals

df = pd.read_csv('population2020.csv')
age_array = df.values
states = ['healthy', 'infected', 'sick', 'recovered', 'dead']


class Person:
    age = 0
    background_sickness = 0
    exposure = 0
    follow_protocol = 0
    quarantine = 0
    state = states[0]

    def __init__(self):
        pass


    def set_values(self):
        self.age = self.set_age()
        # TODO: increase bs when older age
        chance_of_bs = 0.10
        self.background_sickness = 1 if random.uniform(0, 1) < chance_of_bs else 0
        # TODO: increase exposure depending on age
        self.exposure = random.uniform(0, 1)
        # TODO: increase follow_protocol depending on age
        self.follow_protocol = random.uniform(0, 1)
        self.quarantine = 0
        chance_of_inf = 0.01
        self.state = states[1] if random.uniform(0, 1) < chance_of_inf else states[0]


    def set_age(self):
        """
        Sets a random weighted age for the person
        Data collected from ssb.no to get realistic ages
            collected from: https://www.ssb.no/statbank/table/07459/
            date: (21.09.2020)
        ----------
        Return:
            age - int, the age of the person
        """
        weight = []
        ages = []
        for age_group in age_array:
            weight.append(age_group[2])
            ages.append([age_group[0], age_group[1]])
        age_range = random.choices(ages, weights=weight, k=1)
        age = random.randint(age_range[0][0], age_range[0][1])
        return age


    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)


def initialize():
    global todayPersons, nextDayPersons

    todayPersons = np.full((n,n), Person())
    for person in persons:
        p in person:
        p.set_values()
    nextDayPersons = np.full((n,n), Person())

    todayPersons = zeros([n, n])
    for x in range(n):
        for y in range(n):
            todayPersons[x, y] = 1 if random.uniform(0, 1) < p else 0
    nextDayPersons = zeros([n, n])


def observe():
    global todayPersons, nextDayPersons
    cla()
    imshow(todayPersons, vmin = 0, vmax = 1, cmap = cm.binary)


def update():
    global todayPersons, nextDayPersons
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += todayPersons[(x + dx) % n, (y + dy) % n]
            nextDayPersons[x, y] = 1 if count >= 4 else 0
    todayPersons, nextDayPersons = nextDayPersons, todayPersons

#pycxsimulator.GUI().start(func=[initialize, observe, update])
