import matplotlib.pyplot as plt
import const
import numpy as np
from statistics import median


def graph(healthy, infectious, sick, dead, recovered, filename):
	"""
	Creates a graph of the states of all Persons in a population
	:param healthy: list - numbers of healthy Persons per time step
	:param infectious: list - numbers of infectious Persons per time step
	:param sick: list - numbers of sick Persons per time step
	:param dead: list - numbers of dead Persons per time step
	:param recovered: list - numbers of recovered Persons per time step
	:param filename: string - what number the file should be called
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

	plt.savefig("one_run_images/graph_" + str(filename) + '.png')

	plt.show()
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


def plot_fitness_all_generations(dict_data, no_of_gens=None, no_of_parents=4):
	"""
	Plots and saves the fitness for the N best fitnesses for each generation, for all generations
	:param dict_data: the data in a dictionary
	:param no_of_gens: number of generations to be plotted
	:param no_of_parents: number of individuals to be plotted (usually the parents used)
	"""
	if no_of_gens is None:
		no_of_gens = len(dict_data)

	fitness_all = []
	width = 0.15
	y = []
	for i, generation in enumerate(dict_data):
		y.append(i)
		fitness_all.append([])
		for j, individual in enumerate(dict_data[generation]):
			fitness_all[i].append(individual['fitness'])
			if j + 1 == no_of_parents:
				break

	fitness_all = fitness_all[:no_of_gens]

	numpy_array = np.array(fitness_all)
	transpose = numpy_array.T
	fitness_all = transpose.tolist()
	ind = np.arange(no_of_gens)

	for i in range(no_of_parents):
		plt.bar(ind - width + width * i, fitness_all[i], width, label='fitness: ' + str(i + 1))

	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.title(str(no_of_parents) + 'best fitness for all generations')
	label = [str(i + 1) for i in range(no_of_gens)]
	plt.xticks(ind + width / 2, label)
	plt.legend(loc='best')
	plt.savefig("fitness_bar.png")
	plt.show()


def plot_line_avg(data, no_of_gens, population_size):
	"""
	Plots the highest, lowest and average fitness for each generation
	:param data: the data in a dictionary
	:param no_of_gens: number of gens to be plotted
	:param population_size: the size of the population in each generation
	"""
	y = []
	fitness_min = []
	fitness_max = []
	fitness_avg = []
	fitness_med = []
	for i, generation in enumerate(data):
		y.append(i)
		fitness_min.append(data[generation][population_size - 1]['fitness'])
		fitness_max.append(data[generation][0]['fitness'])
		fitness_tot = 0
		total = []
		for j, individual in enumerate(data[generation]):
			fitness_tot += individual['fitness']
			total.append(individual['fitness'])
		fitness_avg.append(sum(total) / len(total))
		fitness_med.append(median(total))
		if i == no_of_gens:
			break
	plt.plot(y, fitness_max, label='fitness max', linestyle='--', color='indianred')
	plt.plot(y, fitness_min, label='fitness min', linestyle='--', color='red')
	plt.plot(y, fitness_avg, label='fitness avgerage', color='darkred')
	plt.plot(y, fitness_med, label='fitness median')
	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.title('Highest, lowest, average and median fitness for ' + str(no_of_gens) + ' generations')
	plt.legend(loc='best')
	plt.savefig("fitness_line.png")
	plt.show()
