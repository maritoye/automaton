import copy
import random

from Person import Person

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from Types import RulesIsolation, RulesQuarantine, Quarantine, PersonState, Gender

CHANCE_OF_GETTING_INFECTION = 0.005


class GroupOfPeople:
    # changable (0-1)
    hygiene = 0
    mask = 0
    distancing = 0
    curfew = 0
    test_rate = 0

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

        self.quarantine_rules = quarantine_rules
        self.isolation_rules = isolation_rules

        for i in range(self.persons.shape[0]):
            for j in range(self.persons.shape[1]):
                self.persons[j][i] = Person(chance_of_infection=CHANCE_OF_GETTING_INFECTION)

    def update(self):
        next_persons = copy.deepcopy(self.persons)
        for y in range(self.persons.shape[0]):
            for x in range(self.persons.shape[1]):
                radius = self.persons[y][x].exposure_radius

                if self.persons[y][x].state == PersonState.HEALTHY:
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
                                break  # I do not think there is a need to through rest of the loop after this condition
                        if next_persons[y][x].state == PersonState.INFECTIOUS:
                            break

                elif self.persons[y][x].state == PersonState.INFECTIOUS:
                    next_persons[y][x].incubation_period -= 1
                    if next_persons[y][x].incubation_period == 0:
                        next_persons[y][x].state = PersonState.SICK

                elif self.persons[y][x].state == PersonState.SICK:
                    next_persons[y][x].recovery_period -= 1
                    if next_persons[y][x].recovery_period == 0:
                        if random.uniform(0, 1) <= self.persons[y][x].get_death_ratio():
                            next_persons[y][x].state = PersonState.DEATH
                        else:
                            next_persons[y][x].state = PersonState.RECOVERED

                next_persons = self.set_quarantine_isolation(x, y, radius, next_persons)

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

    def set_quarantine_isolation(self, x, y, radius, next_persons_copy):
#        if next_persons_copy[y][x].quarantine_count > 0:
#            next_persons_copy[y][x].quarantine_count -= 1
#        if next_persons_copy[y][x].quarantine_count == 0:
#            next_persons_copy[y][x].quarantine = Quarantine.NO

        if next_persons_copy[y][x].state == PersonState.INFECTIOUS:
            if random.uniform(0, 1) < self.test_rate:
                if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or \
                                self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS or \
                                self.quarantine_rules == RulesQuarantine.ALL:
                    next_persons_copy[y][x].quarantine = Quarantine.QUARANTINE
                    #if next_persons_copy[y][x].quarantine_count == 0:
                        #next_persons_copy[y][x].quarantine_count = 10
                if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or \
                                self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS or \
                                self.isolation_rules == RulesIsolation.ALL:
                    next_persons_copy[y][x].quarantine = Quarantine.TOTAL_ISOLATION
                    #next_persons_copy[y][x].quarantine_count = 10

                if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if dy == 0 and dx == 0:
                                continue
                            (next_persons_copy[(y + dy) % self.persons.shape[0]][
                                 (x + dx) % self.persons.shape[1]]).quarantine = Quarantine.QUARANTINE

                if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if dy == 0 and dx == 0:
                                continue
                            (next_persons_copy[(y + dy) % self.persons.shape[0]][
                                 (x + dx) % self.persons.shape[1]]).quarantine = Quarantine.TOTAL_ISOLATION


        elif next_persons_copy[y][x].state == PersonState.SICK:
            if self.quarantine_rules == RulesQuarantine.SICK or \
                            self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or \
                            self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS or \
                            self.quarantine_rules == RulesQuarantine.ALL:
                next_persons_copy[y][x].quarantine = Quarantine.QUARANTINE
            if self.isolation_rules == RulesIsolation.SICK or \
                            self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or \
                            self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS or \
                            self.isolation_rules == RulesIsolation.ALL:
                next_persons_copy[y][x].quarantine = Quarantine.TOTAL_ISOLATION

            if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS:
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        if dy == 0 and dx == 0:
                            continue
                        (next_persons_copy[(y + dy) % self.persons.shape[0]][
                            (x + dx) % self.persons.shape[1]]).quarantine = Quarantine.QUARANTINE

            if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS:
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        if dy == 0 and dx == 0:
                            continue
                        (next_persons_copy[(y + dy) % self.persons.shape[0]][
                             (x + dx) % self.persons.shape[1]]).quarantine = Quarantine.TOTAL_ISOLATION

        if self.quarantine_rules == RulesQuarantine.ALL:
            next_persons_copy[y][x].quarantine = Quarantine.QUARANTINE

        if self.isolation_rules == RulesIsolation.ALL:
            next_persons_copy[y][x].quarantine = Quarantine.TOTAL_ISOLATION

# TODO: remove quarantines somehow (now people just stay quarantined and isolated forever...)

        return next_persons_copy

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
                'vulnerability_ratio': (1 - dp.risk_of_getting_infected) * dp.follow_protocol,
                'background_sickness': dp.background_sickness,
                'smoking': True if dp.smoking else False,
                'overweight': True if dp.bmi else False,
                'gender': Gender.MALE if dp.gender == Gender.MALE else Gender.FEMALE
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
