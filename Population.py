import copy
import random

from Person import Person

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from Types import PersonState


class Population:
	# changable (0-1)
	hygiene = 0
	mask = 0
	distancing = 0
	curfew = 0
	test_rate = 0
	# TODO quarantene rules
	# TODO isolation rules

	# non-changable
	healthcare = 0 # access to medications and respirators
	# TODO smoking
	# TODO bmi

	persons = []

	def __init__(self, x, y, healthcare, hygiene, mask, distancing, curfew, test_rate):
		self.healthcare = healthcare
		self.hygiene = hygiene
		self.mask = mask
		self.distancing = distancing
		self.curfew = curfew
		self.test_rate = test_rate

		self.persons = np.ndarray((y, x), dtype=np.object)

		for i in range(self.persons.shape[0]):
			for j in range(self.persons.shape[1]):
				self.persons[j][i] = Person(chance_of_infection=0.05)

	def run(self, step_list):
		count = 0
		while count < 1000:
			count += 1
			self.update()
			if count in step_list:
				#save image
				pass

	def update(self):
		next_persons = copy.deepcopy(self.persons)
		for y in range(self.persons.shape[0]):
			for x in range(self.persons.shape[1]):
				# if person is healthy
				if self.persons[y][x].state == PersonState.HEALTHY:
					radius = self.persons[y][x].exposure
					vulnerability_ratio = self.persons[y][x].get_vulnerability_ratio(self.mask, self.distancing, self.hygiene, self.curfew)
					for dy in range(-radius, radius + 1):
						for dx in range(-radius, radius + 1):
							if dy == 0 and dx == 0:
								continue
							risk_ratio = self.persons[(y + dy) % self.persons.shape[0]][(x + dx) % self.persons.shape[1]].get_risk_ratio(self.mask, self.distancing, self.hygiene, self.curfew)
							if random.uniform(0, 1) <= risk_ratio * vulnerability_ratio:
								next_persons[y][x].state = PersonState.INFECTIOUS
				# if person is infectious
				elif self.persons[y][x].state == PersonState.INFECTIOUS:
					next_persons[y][x].incubation_period -= 1
					if next_persons[y][x].incubation_period == 0:
						next_persons[y][x].state = PersonState.SICK
				# if person is sick
				elif self.persons[y][x].state == PersonState.SICK:
					next_persons[y][x].recovery_period -= 1
					if next_persons[y][x].recovery_period == 0:
						if random.uniform(0,1) <= self.persons[y][x].get_death_ratio():
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
		pass
		# returns no_of_dead, no_of_recovered etc.