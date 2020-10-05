from Person import Person

class Population:
	# changable
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

		self.persons = (["p"] * x for i in range(y))
		for i in range(y):
			for j in range(x):
				self.persons[y][x] = Person



