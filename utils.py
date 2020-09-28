import random
import pandas as pd
from Types import *

df = pd.read_csv('population2020.csv')
age_array = df.values


def set_incubation_time():
    """
    Sets the incubation time for the person
    The incubation time is between 2 and 14 days
    The mean of incubation time is between 3 and 5 days
        source from: https://www.worldometers.info/coronavirus/coronavirus-incubation-period/
        date collected: 28.09.2020
    ----------
    Return:
        int - a weighted random between 2 and 14 with higher weight on 3 and 5
    """
    weight = [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    days = range(2, 15)
    return int(random.choices(days, weights=weight, k=1)[0])


def set_age():
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
    for group in age_array:
        weight.append(group[1])
        ages.append(group[0])
    age = int(random.choices(ages, weights=weight, k=1)[0])
    return age


def get_age_group(age):
    if age in AgeGroup.INFANT.value:
        return AgeGroup.INFANT
    elif age in AgeGroup.CHILD:
        return AgeGroup.CHILD
    elif age in AgeGroup.YOUNG_ADULT:
        return AgeGroup.YOUNG_ADULT
    elif age in AgeGroup.ADULT:
        return AgeGroup.ADULT
    elif age in AgeGroup.MIDDLE_AGE:
        return AgeGroup.MIDDLE_AGE
    elif age in AgeGroup.AGED:
        return AgeGroup.AGED
    elif age in AgeGroup.OLD:
        return AgeGroup.OLD
