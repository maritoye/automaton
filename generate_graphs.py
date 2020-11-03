import matplotlib.pyplot as plt
import const
import numpy as np


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
	plt.plot(x, recovered, color="green", label="Recovered")
	plt.plot(x, dead, color="black", label="Dead")

	plt.xlabel('Time steps')
	plt.ylabel('People')
	plt.axis([0, len(x), 0, healthy[0]+infectious[0]])
	plt.legend()

	plt.savefig("one_run_images/graph.png")

	#plt.show()
	plt.close()


def plot_each_generation(dict_data):
	"""
	Plots one bar graph for all generations
	Plots the number of healthy, infectious, sick, recovered and dead
	Plots for only the 'parents'
	:param dict_data: the data in a dictionary
	"""
	for generation in dict_data:
		healthy = []
		infectious = []
		sick = []
		recovered = []
		dead = []
		for i, individual in enumerate(dict_data[generation]):
			healthy.append(individual['healthy'])
			infectious.append(individual['infectious'])
			sick.append(individual['sick'])
			recovered.append(individual['recovered'])
			dead.append(individual['dead'])
			if i + 1 == const.NUMBER_OF_PARENTS:
				break
		y = []
		for j in range(const.NUMBER_OF_PARENTS):
			y.append(j)
		ind = np.arange(const.NUMBER_OF_PARENTS)
		width = 0.15
		plt.bar(ind - width*1.5, healthy,    width, label='healthy')
		plt.bar(ind - width/2,   infectious, width, label='infectious')
		plt.bar(ind + width/2,   sick,       width, label='sick')
		plt.bar(ind + width*1.5, recovered,  width, label='recovered')
		plt.bar(ind + width*2.5, dead,       width, label='dead')

		plt.xlabel('individual')
		plt.ylabel('no in state')
		plt.title(generation)

		label = [str(i + 1) for i in range(const.NUMBER_OF_PARENTS)]
		plt.xticks(ind + width / 2, label)
		plt.legend(loc='best')
		plt.show()


def plot_fitness_all_generations(dict_data):
	"""
	Plots the fitness for the N best fitnesses for each generation, for all generations
	:param dict_data: the data in a dictionary
	"""
	fitness_all = []
	ind = np.arange(const.NUMBER_OF_GENERATIONS)
	width = 0.15
	y = []
	for i, generation in enumerate(dict_data):
		y.append(i)
		fitness_all.append([])
		for j, individual in enumerate(dict_data[generation]):
			fitness_all[i].append(individual['fitness'])
			if j + 1 == const.NUMBER_OF_PARENTS:
				break

	numpy_array = np.array(fitness_all)
	transpose = numpy_array.T
	fitness_all = transpose.tolist()

	for i in range(const.NUMBER_OF_PARENTS):
		plt.bar(ind - width + width * i, fitness_all[i], width, label='fitness: ' + str(i + 1))

	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.title(str(const.NUMBER_OF_PARENTS) + 'best fitness for all generations')
	label = [str(i + 1) for i in range(const.NUMBER_OF_GENERATIONS)]
	plt.xticks(ind + width / 2, label)
	plt.legend(loc='best')
	plt.show()
	plt.savefig("fitness.png")
