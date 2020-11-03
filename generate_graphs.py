import matplotlib.pyplot as plt


def graph(healthy, infectious, sick, dead, recovered):
	"""
	Creates a graph of the states of all Persons in a population
	:param healthy: list - numbers of healthy Persons per time step
	:param infectious: list - numbers of infectious Persons per time step
	:param sick: list - numbers of sick Persons per time step
	:param dead: list - numbers of dead Persons per time step
	:param recovered: list - numbers of recovered Persons per time step
	"""
	x = [i for i in range(len(healthy))]

	plt.plot(x, healthy, color="gray", label="Healthy")
	plt.plot(x, infectious, color="yellow", label="Infectious")
	plt.plot(x, sick, color="red", label="Sick")
	plt.plot(x, dead, color="black", label="Dead")
	plt.plot(x, recovered, color="green", label="Recovered")

	plt.xlabel('Time steps')
	plt.ylabel('People')
	plt.axis([0, len(x), 0, healthy[0]+infectious[0]])
	plt.legend()

	plt.savefig("one_run_images/graph.png")

	#plt.show()
	plt.close()