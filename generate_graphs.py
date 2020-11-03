import matplotlib.pyplot as plt


def graph(healthy, infectious, sick, dead, recovered):
	"""
	creates a graph of the states of all Persons in a population
	:param healthy: list - numbers of healthy Persons per timestep
	:param infectious: list - numbers of infectious Persons per timestep
	:param sick: list - numbers of sick Persons per timestep
	:param dead: list - numbers of dead Persons per timestep
	:param recovered: list - numbers of recovered Persons per timestep
	:return:
	"""
	x = [i for i in range(len(healthy))]

	plt.plot(x, healthy, color="gray", label="Healthy")
	plt.plot(x, infectious, color="yellow", label="Infectious")
	plt.plot(x, sick, color="red", label="Sick")
	plt.plot(x, recovered, color="green", label="Recovered")
	plt.plot(x, dead, color="black", label="Dead")

	plt.xlabel('Time steps')
	plt.ylabel('People')
	plt.axis([0, len(x), 0, healthy[0]+infectious[0]])
	plt.legend()

	plt.savefig("one_run_images/graph.png")

	plt.show()
	plt.close()