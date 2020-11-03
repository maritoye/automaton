from GroupOfPeople import GroupOfPeople
from Types import RulesQuarantine
import random
import const
import save_data as save
import main_one_run


def run_generations(initial_population):
	"""
	Runs NUMBER_OF_GENERATIONS amount of generations. For each individual in the generation, update
	TIME_STEP_GROUPOFPEOPLE time steps, then get the fitness. Sorts the individuals by fitness score.
	Get the brief statistics of all the individuals. Create the next population from the parents.
	:param initial_population: list of instances of GroupOfPeople with length population_size
	"""
	all_individuals = []
	current_population = initial_population

	data = {}
	for generation in range(const.NUMBER_OF_GENERATIONS):
		data['generation' + str(generation + 1)] = []
		print(f"\nGeneration %g:" % (generation+1))

		for i in range(const.POPULATION_SIZE):
			for step in range(const.TIME_STEPS_GROUPOFPEOPLE):
				current_population[i].update()
			current_population[i].get_fitness()

		current_population.sort(key=lambda gop: gop.fitness, reverse=True)

		current_population_statistics = []
		for i in range(const.POPULATION_SIZE):
			current_population_statistics.append(current_population[i].get_brief_statistics())
			data['generation' + str(generation + 1)].append(current_population[i].get_brief_statistics2())
			print("\nIndividual %i:" % (i+1))
			print(f"Fitness: %f" % (current_population_statistics[i]['fitness']))
			print("Parameters: ")
			print(current_population_statistics[i])

		all_individuals.append(current_population_statistics)
		parents = current_population_statistics[:const.NUMBER_OF_PARENTS]
		current_population = create_population(parents)

	save.save_run(all_individuals, const.RUN_DATA)
	save.write_to_json(data)

	main_one_run.one_run(const.X, const.Y, parents[0]["healthcare"],parents[0]["hygiene"],parents[0]["mask"],
						 parents[0]["distancing"],parents[0]["curfew"],parents[0]["test_rate"],
						 parents[0]["quarantine_rules"],parents[0]["isolation_rules"])




def create_population(parents):
	"""
	Creates a new population with population_size amount of offsprings, from parents
	:param parents: list of dicts, of length number_of_parents - each dict is the statistics for one instance of GroupOfPoeple
	:return: list of instances of GroupOfPeople with length population_size
	"""
	new_population = []

	for new_offspring in range(const.POPULATION_SIZE):
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
	Does crossover by choosing genes randomly from the parents, with a probability of each parents gene being chosen
	given by the parent_weights list
	:param parents: list of dict, of length number_of_parents - each dict is the statistics for one instance of GroupOfPoeple
	:return: dict - containing a full set of genes which is a crossover of the parents genes
	"""
	crossover_genes = {}
	parent_weights = set_parent_weights(parents)

	for gene in const.GENE_TYPES:
		parent_for_this_gene = parent_weights[random.randint(0,len(parent_weights)-1)]
		value = parents[parent_for_this_gene][gene]
		crossover_genes[gene] = value

	return crossover_genes


def mutation(chromosome):
	"""
	mutates each gene in a set of genes, each with a probability of mutation_probability. If mutation is chosen the gene
	will mutate a maximum of max_mutation
	:param chromosome: dict - one full set of genes
	:return: dict - one full set of genes
	"""
	mutated_genes = {'x':const.X, 'y':const.Y}

	for gene_type in const.GENE_TYPES:

		if gene_type != 'quarantine_rules' and gene_type != 'isolation_rules':
			value = chromosome[gene_type]
			if random.uniform(0,1) < const.MUTATION_PROBABILITY:
				new_value = random.uniform(value - const.MAX_MUTATION, value + const.MAX_MUTATION)
				if new_value > 1:
					new_value = 1
				elif new_value < 0:
					new_value = 0
				mutated_genes[gene_type] = new_value
			else:
				mutated_genes[gene_type] = value
		else:
			value = chromosome[gene_type].value
			if random.uniform(0,1) < const.MUTATION_PROBABILITY:
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
	Creates a list with fitness/FITNESS_ACCURACY number of instances for each of the parents,
	for having higher probability of choosing genes of a parent if the parent has high fitness.
	:param parents: list of dict, of length number_of_parents - each dict is the statistics for one instance of GroupOfPoeple
	:return: list of int
	"""
	parent_weights = []

	for i in range(const.NUMBER_OF_PARENTS):
		fitness = parents[i]['fitness']
		probability_of_parent = fitness//const.FITNESS_ACCURACY
		for j in range(probability_of_parent):
			parent_weights.append(i)

	return parent_weights