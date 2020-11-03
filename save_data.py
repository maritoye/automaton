import const
import json
import numpy as np
import matplotlib.pyplot as plt


def save_run(all_list, run_data):
	"""
	Saves the data results for the evolutionary algorithm, for analyzing and plotting graphs etc
	:param parent_list: List with statistics of all chosen parents of each generation
	:param all_list: List - all statistics of all individuals in each generation
	:param run_data: Dict - constants used for running evolutionary algorithm
	"""
	new_file = open("evolutionary_run.txt","w")

	new_file.writelines("{'run_data':" + str(run_data) + "}" + '\n')

	current = 0
	for gen in range(const.NUMBER_OF_GENERATIONS):
		for individual in range(const.POPULATION_SIZE):
			new_file.writelines(str(all_list[gen][current]) + '\n')
			current += 1
		current = 0

	new_file.close()


def write_to_json(data):
	json_object = json.dumps(data, indent = 4)
	with open('data.json', 'w') as outfile:
		outfile.write(json_object)
		outfile.close()


def read_from_json(datafile):
	with open(datafile, 'r') as openfile:
		json_object = json.load(openfile)
	return json_object


def plot_each_generation(dict_data):
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

	for i in range(const.NUMBER_OF_GENERATIONS):
		print(fitness_all[i])

	numpy_array = np.array(fitness_all)
	transpose = numpy_array.T
	fitness_all = transpose.tolist()

	for i in range(const.NUMBER_OF_PARENTS):
		print(fitness_all[i])
		plt.bar(ind - width + width * i, fitness_all[i], width, label='fitness: ' + str(i + 1))

	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.title(str(const.NUMBER_OF_PARENTS) + 'best fitness for all generations')
	label = [str(i + 1) for i in range(const.NUMBER_OF_GENERATIONS)]
	plt.xticks(ind + width / 2, label)
	plt.legend(loc='best')
	plt.show()


data_json = read_from_json('data.json')
plot_fitness_all_generations(data_json)

