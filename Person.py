from Types import PersonState, Quarantine
import random
from utils import *

p = 0.1


class Person:
    age = 0
    age_group = 0
    background_sickness = 0
    exposure = 0  # How active one person is
    follow_protocol = 0
    quarantine = 0
    state = PersonState.EMPTY
    state_count = 0
    gender = 0
    exposure_ratio = 0
    vulnerability_ratio = 0
    death_ratio = 0
    incubation_period = 0  # 2-14 (3-5 har mye vekt)
    bmi = 0
    smoking = 0

    def __init__(self):
        pass

    def generate_random_values(self):
        self.age = self.set_age()
        self.age_group = get_age_group(self.age)
        self.background_sickness = get_background_sickness(self.age)
        self.exposure = random.randint(1, 3)

        # TODO: increase follow_protocol depending on age
        self.follow_protocol = random.uniform(0, 1)
        self.quarantine = 0
        self.gender = Gender.FEMALE if random.random() < 0.5 else Gender.MALE

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
            # if(self.follow_protocol == )

        pass

    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
