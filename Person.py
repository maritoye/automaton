import pandas as pd
import random

n = 10
from Types import PersonState, Quarantine, Gender
import random
import utils


class Person:
    age = 0
    age_group = 0
    background_sickness = 0
    exposure_radius = 0  # How active one person is
    follow_protocol = 0
    quarantine = 0
    state = PersonState.EMPTY
    gender = 0
    exposure_ratio = 0
    vulnerability_ratio = 0
    death_ratio = 0
    incubation_period = 0  # 2-14 (3-5 har mye vekt) vanligvis ikke over 9
    recovery_period = 0
    bmi = 0
    smoking = 0

    def __init__(self, chance_of_infection):
        self.age = utils.set_age()
        self.age_group = utils.get_age_group(self.age)
        self.background_sickness = utils.get_background_sickness(self.age)
        # self.exposure = random.randint(1, 3) # how big (1 - one ring, 3 - three rings) the ´social ring´ is for current person
        self.exposure_radius = random.randint(1, 3) # how big (1 - one ring, 3 - three rings) the ´social ring´ is for current person
        self.follow_protocol = utils.get_adherence(self.age)
        self.smoking = utils.get_smoking(self.age)
        self.bmi = utils.get_obesity(self.age)
        self.quarantine = 0
        self.gender = Gender.FEMALE if random.random() < 0.5 else Gender.MALE

        # self.state = states[1] if random.uniform(0, 1) < chance_of_inf else states[0]
        self.state = PersonState.INFECTIOUS if random.uniform(0, 1) < chance_of_infection else PersonState.HEALTHY
        self.incubation_period = random.randint(2, 14)
        self.recovery_period = random.randint(7, 28)

    def get_vulnerability_ratio(self, mask, distancing, hygiene, curfew):
        # risk of getting infected  0 no risk, 1 = highest risk
        vulnerability_ratio = (mask + distancing + hygiene + curfew) / 4
        return (1 - vulnerability_ratio) * self.follow_protocol

    def get_risk_ratio(self, mask, distancing, hygiene, curfew):
        # risk of infecting others 0 no risk, 1 = highest risk
        if self.state not in [PersonState.SICK, PersonState.INFECTIOUS]:
            return 0
        else:
            if self.quarantine == Quarantine.TOTAL_ISOLATION:
                # any chance of people breaking isolation?
                # what about people you live with? are they also isolated, or quarantined
                # in those cases they can be infected...
                return 0

                # TODO or Not TODO? That is the question

            elif self.quarantine == Quarantine.QUARANTINE:
                # how strict is the quarantine? (can you go to stores, be with others)
                # how strictly do you follow protocols?
                return 1 - (self.follow_protocol / 2)

            # if infected or sick but not in quarantine or isolation
            else:
                protocols = (distancing + mask + hygiene) / 3
                # social distancing rules =
                # face mask rules / recommendations
                # + distancing (i.e one meter rule)
                # + hygiene rules

                risk_ratio = (1 - protocols) * (1 - self.follow_protocol)
                # following protocols * social distancing rules
                # + exposure??
                # + staying at home rules (i.e portforbud) (can be part of the exposure variable??)
                return risk_ratio

    def get_death_ratio(self):
        # background_sickness, maybe age, lifestyle (smoking, weight), health care (respirator, medicines)
        # https://www.fhi.no/contentassets/8a971e7b0a3c4a06bdbf381ab52e6157/vedlegg/andre-halvar-2020/2020.09.23-ukerapport-uke-38-covid-19.pdf
        # page 24
        # 1.38% som får corona dør av det. 87% av desse har underliggende sykdom
        # if the person is smoking, increase the chance of death by 5%
        # if the person is overweight, increase the chance of death by 5%
        if self.background_sickness:
            self.death_ratio = 0.0120006 * (0.01 * self.age) + 0.05 if self.smoking else 0 + 0.05 if self.bmi else 0
            # TODO adjust by age
        else:
            self.death_ratio = 0.001794 * (0.01 * self.age) + 0.05 if self.smoking else 0 + 0.05 if self.bmi else 0

        return self.death_ratio

    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure_radius)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
