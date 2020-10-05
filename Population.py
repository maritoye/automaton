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
	healthcare = 0 # access to medications
	# TODO smoking
	# TODO bmi

	persons = []

	def __init__(self):
		

	def set_hygiene(self, hygiene):
		self.hygiene = hygiene

	def set_mask(self, mask):
		self.mask = mask

	def set_distancing(self, distancing):
		self.distancing = distancing

	def set_curfew(self, curfew):
		self.curfew = curfew

	def set_test_rate(self, test_rate):
		self.test_rate = test_rate

