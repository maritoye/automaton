import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from Person import Person
from Types import RulesIsolation, RulesQuarantine, Quarantine, PersonState
from utils import fitness_function_with_cost
from utils import fitness_function
import const


class GroupOfPeople:

    def __init__(self, x, y, healthcare, hygiene, mask, distancing, curfew, test_rate, quarantine_rules,
                 isolation_rules):
        self.healthcare = healthcare
        self.hygiene = hygiene
        self.mask = mask
        self.distancing = distancing
        self.curfew = curfew
        self.test_rate = test_rate

        self.quarantine_rules = quarantine_rules
        self.isolation_rules = isolation_rules
        self.fitness = 0

        while True:
            any_infected = False
            self.persons = np.ndarray((y, x), dtype=np.object)
            for i in range(self.persons.shape[0]):
                for j in range(self.persons.shape[1]):
                    self.persons[i][j] = Person(chance_of_infection=const.CHANCE_OF_INITIAL_INFECTION)
                    if any_infected is False and self.persons[i][j].state == PersonState.INFECTIOUS:
                        any_infected = True
            if any_infected:
                break

    def update(self):
        """
        Updates the model with one step
        Includes all the rules for which people to be infected, sick, recover or die
        """
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
                                break
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

    def observe(self, time_step):
        """
        Used for visualizing the grid of Person object states
        :param time_step: the current time step for the visualization, used for saving png
        """
        foo = np.ndarray(self.persons.shape, dtype=np.int)
        for y in range(self.persons.shape[0]):
            for x in range(self.persons.shape[1]):
                foo[y][x] = self.persons[y][x].state.value
        cmap = colors.ListedColormap(['b', 'w', 'y', 'r', 'g', 'k'])
        plt.imshow(foo, vmin=0, vmax=5, cmap=cmap)

        name = "one_run_images/ca_time_step_" + str(time_step) + ".png"
        plt.savefig(name)
        plt.show()
        plt.close()

    def set_quarantine_isolation(self, x, y, radius, next_persons):
        """
        The rules for setting people in quarantine and isolation
        """
        if next_persons[y][x].quarantine_count > 0:
            next_persons[y][x].quarantine_count -= 1
        if next_persons[y][x].quarantine_count == 0:
            next_persons[y][x].quarantine = Quarantine.NO

        if next_persons[y][x].state == PersonState.INFECTIOUS:
            if random.uniform(0, 1) < self.test_rate:
                if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or \
                                self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS or \
                                self.quarantine_rules == RulesQuarantine.ALL:
                    self.set_count(next_persons[y][x], (Quarantine.TOTAL_ISOLATION or Quarantine.QUARANTINE), Quarantine.QUARANTINE, const.QUARANTINE_DURATION)

                if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or \
                                self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS or \
                                self.isolation_rules == RulesIsolation.ALL:
                    self.set_count(next_persons[y][x], Quarantine.TOTAL_ISOLATION, Quarantine.TOTAL_ISOLATION, const.ISOLATION_DURATION)

                if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if not (dy == 0 and dx == 0):
                                neighbor = (
                                    next_persons[(y + dy) % self.persons.shape[0]][(x + dx) % self.persons.shape[1]])
                                self.set_count(neighbor, (Quarantine.TOTAL_ISOLATION or Quarantine.QUARANTINE), Quarantine.QUARANTINE, const.QUARANTINE_DURATION)

                if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if not (dy == 0 and dx == 0):
                                neighbor = (
                                    next_persons[(y + dy) % self.persons.shape[0]][(x + dx) % self.persons.shape[1]])
                                self.set_count(neighbor, Quarantine.TOTAL_ISOLATION, Quarantine.TOTAL_ISOLATION, const.ISOLATION_DURATION)

        elif next_persons[y][x].state == PersonState.SICK:
            if self.quarantine_rules == RulesQuarantine.SICK or \
                            self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS or \
                            self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS or \
                            self.quarantine_rules == RulesQuarantine.ALL:
                self.set_count(next_persons[y][x],(Quarantine.TOTAL_ISOLATION or Quarantine.QUARANTINE), Quarantine.QUARANTINE, const.QUARANTINE_DURATION)

            if self.isolation_rules == RulesIsolation.SICK or \
                            self.isolation_rules == RulesIsolation.SICK_INFECTIOUS or \
                            self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS or \
                            self.isolation_rules == RulesIsolation.ALL:
                self.set_count(next_persons[y][x], Quarantine.TOTAL_ISOLATION, Quarantine.TOTAL_ISOLATION, const.ISOLATION_DURATION)

            if self.quarantine_rules == RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS:
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        if not (dy == 0 and dx == 0):
                            neighbor = (
                                next_persons[(y + dy) % self.persons.shape[0]][(x + dx) % self.persons.shape[1]])
                            self.set_count(neighbor, (Quarantine.TOTAL_ISOLATION or Quarantine.QUARANTINE), Quarantine.QUARANTINE, const.QUARANTINE_DURATION)

            if self.isolation_rules == RulesIsolation.SICK_INFECTIOUS_NEIGHBORS:
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        if not (dy == 0 and dx == 0):
                            neighbor = (
                                next_persons[(y + dy) % self.persons.shape[0]][(x + dx) % self.persons.shape[1]])
                            self.set_count(neighbor, Quarantine.TOTAL_ISOLATION, Quarantine.TOTAL_ISOLATION, const.ISOLATION_DURATION)

        if self.quarantine_rules == RulesQuarantine.ALL:
            next_persons[y][x].quarantine = Quarantine.QUARANTINE

        if self.isolation_rules == RulesIsolation.ALL:
            next_persons[y][x].quarantine = Quarantine.TOTAL_ISOLATION

        return next_persons

    def set_count(self, person, if_type, set_type, count):
        """
        Sets the state count for a Person object
        :param person: object - the Person object to be updated
        :param if_type: if the person is not in given type
        :param set_type: the type the person should be set to
        :param count: how long the person should be in current state
        """
        if person.quarantine != if_type:
            person.quarantine = set_type
            if person.quarantine_count == 0:
                person.quarantine_count = count

    def get_brief_statistics(self):
        """
        Adds up amount of people in each state, and returns the statistics.
        :return: dict - fitness, states, and variables for the GroupOfPeople
        """
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
            'fitness': int(self.fitness),
            'healthy': healthy_people,
            'infectious': infectious_people,
            'sick': sick_people,
            'recovered': recovered_people,
            'dead': dead_people,
            'healthcare': self.healthcare,
            'hygiene': self.hygiene,
            'mask': self.mask,
            'distancing': self.distancing,
            'curfew': self.curfew,
            'test_rate': self.test_rate,
            'quarantine_rules': self.quarantine_rules,
            'isolation_rules': self.isolation_rules,
        }

    def get_visualization_statistics(self):
        """
        Adds up amount of people in each state, and returns the statistics.
        :return: dict - fitness, states, and variables for visualizing the data
        """
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
            'fitness': int(self.fitness),
            'healthy': healthy_people,
            'infectious': infectious_people,
            'sick': sick_people,
            'recovered': recovered_people,
            'dead': dead_people,
            'healthcare': self.healthcare,
            'hygiene': self.hygiene,
            'mask': self.mask,
            'distancing': self.distancing,
            'curfew': self.curfew,
            'test_rate': self.test_rate,
            'quarantine_rules': self.quarantine_rules.value,
            'isolation_rules': self.isolation_rules.value,
        }

    def get_fitness(self):
        self.fitness = fitness_function_with_cost(self.get_brief_statistics(), self.healthcare, self.hygiene, self.mask,
                                        self.distancing, self.curfew, self.test_rate, self.quarantine_rules, self.isolation_rules)

        #self.fitness = fitness_function(self.get_brief_statistics())
        return self.fitness
