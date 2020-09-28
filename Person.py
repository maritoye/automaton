from Types import PersonState,Quarantine
import pandas as pd
import random

p = 0.1

df = pd.read_csv('population2020.csv')
age_array = df.values


class Person:
    age = 0
    background_sickness = 0
    exposure = 0
    follow_protocol = 0
    quarantine = 0
    state = PersonState.EMPTY
    state_count = 0
    gender = 0
    vulnerability_ratio = 0
    incubation_period = 0
    risk_ratio = 0

    def __init__(self):
        pass


    def generate_random_values(self):
        self.age = self.set_age()
        # self.gender =
        # TODO: increase bs when older age
        chance_of_bs = 0.10
        self.background_sickness = 1 if random.uniform(0, 1) < chance_of_bs else 0
        # TODO: increase exposure depending on age
        self.exposure = random.uniform(0, 1)
        # TODO: increase follow_protocol depending on age
        self.follow_protocol = random.uniform(0, 1)
        self.quarantine = 0

        chance_of_inf = p
        #self.state = states[1] if random.uniform(0, 1) < chance_of_inf else states[0]
        self.state = PersonState.INFECTIOUS if random.uniform(0, 1) < chance_of_inf else PersonState.HEALTHY
        self.state_count = 0


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
        for group in age_array:
            weight.append(group[1])
            ages.append(group[0])
        age = int(random.choices(ages, weights=weight, k=1)[0])
        return age


    def get_vulnerability_ratio(self):
        pass


    def get_risk_ratio(self):
        if self.person_state not in [PersonState.SICK,PersonState.INFECTIOUS]:
            return 0
        else:
            if self.quarantine == Quarantine.TOTAL_ISOLATION:
                return 0

        pass



    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
