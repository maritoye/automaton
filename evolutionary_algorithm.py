from GroupOfPeople import GroupOfPeople
from Types import RulesQuarantine
import random
import const


def run_generations(initial_population):
	"""
	Runs numberOfGeneration amount of generations
	:param initial_population: list of instances of GroupOfPeople
	:return:
	"""

	current_population = initial_population

#	all_time_best = {}

	for generation in range(const.number_of_generations):
		print(f"\nGeneration %g:" % (generation+1))
		for step in range(100):
			for i in range(const.population_size):
				current_population[i].update()

		for i in range(const.population_size):
			current_population[i].get_fitness()
			current_population.sort(key=lambda gop: gop.fitness, reverse=True)

#		if all_time_best:
#			if all_time_best.get_fitness() < current_population[0].get_fitness():
#				all_time_best = current_population[0]
#			else:
#				current_population.append(all_time_best)
#				current_population.sort(key=lambda gop: gop.fitness, reverse=True)
#
#		else:
#			all_time_best = current_population[0]

		for i in range(const.population_size):
			current_population[i].get_fitness()
			current_population[i] = current_population[i].get_brief_statistics()
			print("\nIndividual %i:" % (i+1))
			print(f"Fitness: %f" % (current_population[i]['fitness']))
			print("Parameters: ")
			print(current_population[i])

		parents = current_population[:const.number_of_parents]

		current_population = create_population(parents)


def create_population(parents):
	"""

	:param parents:
	:return:
	"""
	new_population = []

	for new_offspring in range(const.population_size):
		crossover_genes = crossover(parents)
		offspring_genes = mutation(crossover_genes)
		offspring = GroupOfPeople(offspring_genes['x'],offspring_genes['y'],offspring_genes['healthcare'],
								  offspring_genes['hygiene'],offspring_genes['mask'],offspring_genes['distancing'],
								  offspring_genes['curfew'],offspring_genes['test_rate'],
								  RulesQuarantine(offspring_genes['quarantine_rules']),
								  RulesQuarantine(offspring_genes['isolation_rules']))
		new_population.append(offspring)

	return new_population


def crossover(parents):
	"""

	:param parents:
	:return:
	"""
	crossover_genes = {}
	parent_weights = []

	for i in range(const.number_of_parents):
		parent_weights = set_parent_weights(parents)

	for gene in const.gene_types:
		parent_for_this_gene = parent_weights[random.randint(0,len(parent_weights)-1)]
		value = parents[parent_for_this_gene][gene]
		crossover_genes[gene] = value

	return crossover_genes


def mutation(genes):
	"""

	:param genes:
	:return:
	"""
	mutated_genes = {'x':const.x, 'y':const.y}

	for gene_type in const.gene_types:

		if gene_type != 'quarantine_rules' and gene_type != 'isolation_rules':
			value = genes[gene_type]
			if random.uniform(0,1) < const.mutation_probability:
				new_value = random.uniform(value-const.max_mutation,value+const.max_mutation)
				if new_value > 1:
					new_value = 1
				elif new_value < 0:
					new_value = 0
				mutated_genes[gene_type] = new_value
			else:
				mutated_genes[gene_type] = value
		else:
			value = genes[gene_type].value
			if random.uniform(0,1) < const.mutation_probability:
				new_value = random.randint(value-1,value+1)
				if new_value > 4:
					new_value = 4
				elif new_value < 0:
					new_value = 0
				mutated_genes[gene_type] = new_value
			else:
				mutated_genes[gene_type] = value

	return mutated_genes


def set_parent_weights(parents):
	"""

	:param parents:
	:return:
	"""
	parent_weights = []

	for i in range(const.number_of_parents):
		fitness = parents[i]['fitness']
		probability_of_parent = fitness//200
		for j in range(probability_of_parent):
			parent_weights.append(i)

	return parent_weights