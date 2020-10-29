import pandas as pd

from Types import PersonState, Quarantine, Gender
import random
import utils


class Person:

    def __init__(self, chance_of_infection):
        self.age = utils.set_age()
        self.age_group = utils.get_age_group(self.age)  # TODO We only set this property but we did not use it!
        self.background_sickness = utils.get_background_sickness(self.age)
        # how big (1 - one ring, 3 - three rings) the ´social ring´ is for current person
        self.exposure_radius = random.randint(1, 3)
        self.follow_protocol = utils.get_adherence(self.age)
        self.smoking = utils.get_smoking(self.age)
        self.bmi = utils.get_obesity(self.age)
        self.quarantine = Quarantine.NO
        self.gender = Gender.FEMALE if random.uniform(0, 1) < 0.5 else Gender.MALE
        self.quarantine_count = 0

        self.state = PersonState.INFECTIOUS if random.uniform(0, 1) < chance_of_infection else PersonState.HEALTHY
        self.incubation_period = random.randint(2, 14)
        self.recovery_period = random.randint(7, 28)
        self.risk_of_infecting_others = 0
        self.risk_of_getting_infected = 0
        self.death_ratio = self.set_death_ratio()

    def get_vulnerability_ratio(self, mask, distancing, hygiene, curfew):
        # risk of getting infected  0 no risk, 1 = highest risk
        self.risk_of_getting_infected = (1 - ((mask + distancing + hygiene + curfew + self.follow_protocol)/5)) * 0.7
        return self.risk_of_getting_infected

    def get_risk_ratio(self, mask, distancing, hygiene, curfew):
        # risk of infecting others 0 no risk, 1 = highest risk
        if self.state not in [PersonState.SICK, PersonState.INFECTIOUS]:
            self.risk_of_infecting_others = 0
            return self.risk_of_infecting_others
        else:
            if self.quarantine == Quarantine.TOTAL_ISOLATION:
                self.risk_of_infecting_others = 0
                return self.risk_of_infecting_others

            elif self.quarantine == Quarantine.QUARANTINE:
                self.risk_of_infecting_others = (1 - self.follow_protocol) * 0.2
                return self.risk_of_infecting_others

            # if infected or sick but not in quarantine or isolation:
            else:
                self.risk_of_infecting_others = (1 - ((distancing + mask + hygiene + curfew + self.follow_protocol)/5)) * 0.7
                return self.risk_of_infecting_others

    def set_death_ratio(self):
        """
        Background\_sickness, maybe age, lifestyle (smoking, weight), health care (respirator, medicines)
        https://www.fhi.no/contentassets/8a971e7b0a3c4a06bdbf381ab52e6157/vedlegg/andre-halvar-2020/2020.09.23-ukerapport-uke-38-covid-19.pdf
        page 24
        1.38% som får corona dør av det. 87% av desse har underliggende sykdom
        If the person is smoking, increase the chance of death by 5%
        If the person is overweight, increase the chance of death by 5%
        :return:
        """
        if self.background_sickness:
            return 0.0120006 * (
                    0.01 * self.age) + 0.05 if self.smoking else 0 + 0.05 if self.bmi else 0 + 0.02 if self.gender == Gender.MALE else 0
        else:
            return 0.001794 * (
                    0.01 * self.age) + 0.05 if self.smoking else 0 + 0.05 if self.bmi else 0 + 0.02 if self.gender == Gender.MALE else 0

    def get_death_ratio(self):
        return self.death_ratio

    def print_self(self):
        print('Age =', self.age)
        print('bs =', self.background_sickness)
        print('Exposure =', self.exposure_radius)
        print('Follow protocol =', self.follow_protocol)
        print('In quarantine =', self.quarantine)
        print('State =', self.state)
        print('Gender =', self.gender)
