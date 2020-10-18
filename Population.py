import copy
import random

from Person import Person

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from Types import PersonState, RulesIsolation, RulesQuarantine, Quarantine


class Population:
    # changable (float 0-1)
    hygiene = 0
    mask = 0
    distancing = 0
    curfew = 0
    test_rate = 0

    # changable (enum 0-4)
    quarantine_rules = RulesQuarantine.NOONE
    isolation_rules = RulesIsolation.NOONE

    # non-changable
    healthcare = 0  # access to medications and respirators
    # TODO smoking
    # TODO bmi

    persons = []

    def __init__(self, x, y, healthcare, hygiene, mask, distancing, curfew, test_rate, quarantine_rules, isolation_rules):
        self.healthcare = healthcare
        self.hygiene = hygiene
        self.mask = mask
        self.distancing = distancing
        self.curfew = curfew
        self.test_rate = test_rate
        self.persons = np.ndarray((y, x), dtype=np.object)

        self.quarantine_rules = quarantine_rules #TODO: is this correct?
        self.isolation_rules = isolation_rules #TODO: is this correct?


        for i in range(self.persons.shape[0]):
            for j in range(self.persons.shape[1]):
                self.persons[j][i] = Person(chance_of_infection=0.005)

    def run(self, step_list):
        count = 0
        while count < 1000:
            count += 1
            self.update()
            if count in step_list:
                # save image
                pass

    def update(self):
        next_persons = copy.deepcopy(self.persons)
        for y in range(self.persons.shape[0]):
            for x in range(self.persons.shape[1]):
                # if person is healthy
                if self.persons[y][x].state == PersonState.HEALTHY:
                    radius = self.persons[y][x].exposure_radius
                    vulnerability_ratio = self.persons[y][x].get_vulnerability_ratio(self.mask, self.distancing,
                                                                                     self.hygiene, self.curfew)
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if dy == 0 and dx == 0:
                                continue
                            risk_ratio = self.persons[(y + dy) % self.persons.shape[0]][
                                (x + dx) % self.persons.shape[1]].get_risk_ratio(self.mask, self.distancing,
                                                                                 self.hygiene, self.curfew)
                            if random.uniform(0, 1) <= risk_ratio * vulnerability_ratio:
                                next_persons[y][x].state = PersonState.INFECTIOUS

                # if person is infectious
                elif self.persons[y][x].state == PersonState.INFECTIOUS:

                    #TODO should we have clearer rules on when we now they are infectious (given test rate and how long they have been infections)
                    if self.test_rate > 0.5 and next_persons[y][x].incubation_period<3:
                        if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or self.quarantine_rules == RulesQuarantine.SICK_INFECTION_NEIGHBORS or self.quarantine_rules == RulesQuarantine.ALL:
                            next_persons[y][x].quarantine = Quarantine.QUARANTINE
                        if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or self.isolation_rules == RulesIsolation.SICK_INFECTION_NEIGHBORS or self.isolation_rules == RulesIsolation.ALL:
                            next_persons[y][x].quarantine = Quarantine.TOTAL_ISOLATION

                    next_persons[y][x].incubation_period -= 1
                    if next_persons[y][x].incubation_period == 0:
                        next_persons[y][x].state = PersonState.SICK

                # if person is sick
                elif self.persons[y][x].state == PersonState.SICK:

                    # TODO should the test rate determine when we know if they know they are sick?
                    # TODO (so they know whether to apply the quarantine and isolation rules or not)

                    if self.quarantine_rules == RulesQuarantine.SICK or self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or self.quarantine_rules == RulesQuarantine.SICK_INFECTION_NEIGHBORS or self.quarantine_rules == RulesQuarantine.ALL:
                        next_persons[y][x].quarantine = Quarantine.QUARANTINE
                    if self.isolation_rules == RulesIsolation.SICK or self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or self.isolation_rules == RulesIsolation.SICK_INFECTION_NEIGHBORS or self.isolation_rules == RulesIsolation.ALL:
                        next_persons[y][x].quarantine = Quarantine.TOTAL_ISOLATION

                    next_persons[y][x].recovery_period -= 1
                    if next_persons[y][x].recovery_period == 0:
                        if random.uniform(0, 1) <= self.persons[y][x].get_death_ratio():
                            next_persons[y][x].state = PersonState.DEATH
                        else:
                            next_persons[y][x].state = PersonState.RECOVERED

        self.persons = next_persons

    def observe(self):
        # plot population
        foo = np.ndarray(self.persons.shape, dtype=np.int)
        for y in range(self.persons.shape[0]):
            for x in range(self.persons.shape[1]):
                foo[y][x] = self.persons[y][x].state.value
        cmap = colors.ListedColormap(['b', 'w', 'y', 'r', 'g', 'k'])
        plt.imshow(foo, vmin=0, vmax=5, cmap=cmap)
        plt.show()

    def get_statistics(self):
        dead_people = []
        for i in range(self.persons.shape[0]):
            for j in range(self.persons.shape[1]):
                if self.persons[i, j].state == PersonState.DEATH:
                    dead_people.append(self.persons[i, j])
        print("Number of deaths= ", len(dead_people))
        dps = []
        for dp in dead_people:
            dps.append({
                'age': dp.age,
                'vulnerability_ratio': (1 - dp.vulnerability_ratio) * dp.follow_protocol,
                'background_sickness': dp.background_sickness,
                'smoking': True if dp.smoking else False,
                'overweight': True if dp.bmi else False
            })
        return dps

    def get_brief_statistics(self):

        healthy_people = 0
        infectious_people = 0
        sick_people = 0
        recovered_people = 0
        dead_people = 0
        for i in range(self.persons.shape[0]):
            for j in range(self.persons.shape[1]):
                if self.persons[i, j].state == PersonState.HEALTHY:
                    healthy_people += 1
                elif self.persons[i, j].state == PersonState.INFECTIOUS:
                    infectious_people += 1
                elif self.persons[i, j].state == PersonState.SICK:
                    sick_people += 1
                elif self.persons[i, j].state == PersonState.RECOVERED:
                    recovered_people += 1
                elif self.persons[i, j].state == PersonState.DEATH:
                    dead_people += 1
        return {
            'healthy': healthy_people,
            'infectious': infectious_people,
            'sick': sick_people,
            'recovered': recovered_people,
            'dead': dead_people
        }
