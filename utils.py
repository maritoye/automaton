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
    elif age in AgeGroup.CHILD.value:
        return AgeGroup.CHILD
    elif age in AgeGroup.YOUNG_ADULT.value:
        return AgeGroup.YOUNG_ADULT
    elif age in AgeGroup.ADULT.value:
        return AgeGroup.ADULT
    elif age in AgeGroup.MIDDLE_AGE.value:
        return AgeGroup.MIDDLE_AGE
    elif age in AgeGroup.AGED.value:
        return AgeGroup.AGED
    elif age in AgeGroup.OLD.value:
        return AgeGroup.OLD


def get_background_sickness(age):
    """
    Gets background sickness depending on age
    Realistic background sickness
    The probability from backgroun_sickness2019.csv is collected from
        source: https://www.ssb.no/statbank/table/11190/tableViewLayout1/
        date: 29.09.2020
    ----------
    Parameters:
        age - int, the age of a paerson
    ----------
    Return:
        BackgroundSickness.YES or NO - Enum, if the person should have a background sickness
    """
    sickness = pd.read_csv('./background_sickness2019.csv').values
    if age in range(0, 16):
        return BackgroundSickness.NO
    for i in range(len(sickness)):
        if age in range(sickness[i][0], sickness[i][1]):
            return BackgroundSickness.YES if random.randint(0, 100) < sickness[i][2] else BackgroundSickness.NO

# TODO calculate the follow protocol: https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2020.25.37.2001607#html_fulltext