import pycxsimulator
from pylab import *
import pandas as pd
import numpy as np
import random

n = 100 # size of space: n x n
p = 0.24 # probability of initially panicky individuals

df = pd.read_csv('population2020.csv')
age_array = df.values


def set_age():
    # statistics gotten from https://www.ssb.no/statbank/table/07459/ (21.09.2020)
    weight = []
    ages = []
    for age_group in age_array:
        weight.append(age_group[2])
        ages.append([age_group[0], age_group[1]])
    age_range = random.choices(ages, weights=weight, k=1)
    age = random.randint(age_range[0][0], age_range[0][1])
    return age


class Person:
    age = set_age()
    chance_of_bc = 0.10
    background_sickness = 1 if random.uniform(0, 1) < chance_of_bc else 0
    exposure = random.uniform(0, 1)


def initialize():
    global config, nextconfig
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random() < p else 0
    nextconfig = zeros([n, n])


def observe():
    global config, nextconfig
    cla()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)


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

#pycxsimulator.GUI().start(func=[initialize, observe, update])
