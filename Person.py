from Types import PersonState, Quarantine
import random
from utils import *

p = 0.1



class Person:
    age = 0
    age_group = 0
    background_sickness = 0
    exposure = 0
    follow_protocol = 0
    quarantine = 0
    state = PersonState.EMPTY
    state_count = 0
    gender = 0
    vulnerability_ratio = 0
    incubation_period = 0  # 2-14 (3-5 har mye vekt)
    risk_ratio = 0
    death_ratio = 0

    def __init__(self):
        pass

    def generate_random_values(self):
        self.age = self.set_age()

        #TODO call the function for age_group
        #if(between 0.3)
        #    age_group = AgeGroup.INFANT

        # TODO: increase bs when older age
        chance_of_bs = 0.10
        self.background_sickness = 1 if random.uniform(0, 1) < chance_of_bs else 0
        # TODO: increase exposure depending on age
        self.exposure = random.uniform(0, 1)
        # TODO: increase follow_protocol depending on age
        self.follow_protocol = random.uniform(0, 1)
        self.quarantine = 0

        chance_of_inf = p
        # self.state = states[1] if random.uniform(0, 1) < chance_of_inf else states[0]
        self.state = PersonState.INFECTIOUS if random.uniform(0, 1) < chance_of_inf else PersonState.HEALTHY
        self.state_count = 0



    def get_vulnerability_ratio(self):
        pass

    def get_risk_ratio(self):
        if self.person_state not in [PersonState.SICK, PersonState.INFECTIOUS]:
            return 0
        else:
            if self.quarantine == Quarantine.TOTAL_ISOLATION:
                return 0
            # TODO or Not TODO?
            # elif self.quarantine == Quarantine.QUARANTINE:
                #if(self.follow_protocol == )

        pass


    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
