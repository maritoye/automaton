import random

from GroupOfPeople import GroupOfPeople
from utils import mutate_parameter, mutate_quarantine_isolation
import random
from Types import RulesQuarantine, RulesIsolation


populationSize = 10
numberOfParents = 4
numberOfGenerations = 25

mutation_probability = 0.7
max_mutation = 0.3

x = 50
y = 50

gene_types = {'healthcare', 'hygiene', 'mask', 'distancing', 'curfew', 'test_rate', 'quarantine_rules', 'isolation_rules'}



def main():
	population = []

	for index in range(populationSize):
		population.append(GroupOfPeople(x=x,
										y=y,
										healthcare=mutate_parameter(0.5, 0.5),
										hygiene=mutate_parameter(0.5, 0.5),
										mask=mutate_parameter(0.5, 0.5),
										distancing=mutate_parameter(0.5, 0.5),
										curfew=mutate_parameter(0.5, 0.5),
										test_rate=mutate_parameter(0.5, 0.5),
										quarantine_rules=RulesQuarantine(mutate_quarantine_isolation(2, 2)),
										isolation_rules=RulesIsolation(mutate_quarantine_isolation(2, 2))))

	run_generations(initial_population=population)


def run_generations(initial_population):

	current_population = initial_population

#	all_time_best = {}

	for generation in range(numberOfGenerations):
		print(f"\nGeneration %g:" % (generation+1))
		for step in range(100):
			for i in range(populationSize):
				current_population[i].update()

		for i in range(populationSize):
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

		for i in range(populationSize):
			current_population[i].get_fitness()
			current_population[i] = current_population[i].get_brief_statistics()
			print("\nIndividual %i:" % (i+1))
			print(f"Fitness: %f" % (int(current_population[i]['fitness'])))
			print("Parameters: ")
			print(current_population[i])

		parents = current_population[:numberOfParents]

		current_population = create_population(parents)


def create_population(parents):
	new_population = []

	for new_offspring in range(populationSize):
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
	crossover_genes = {}
	parent_weights = []

	for i in range(numberOfParents):
		parent_weights = set_parent_weights(parents)

	for gene in gene_types:
		parent_for_this_gene = parent_weights[random.randint(0,len(parent_weights)-1)]
		value = parents[parent_for_this_gene][gene]
		crossover_genes[gene] = value

	return crossover_genes


def mutation(genes):
	mutated_genes = {'x':x, 'y':y}

	for gene_type in gene_types:

		if gene_type != 'quarantine_rules' and gene_type != 'isolation_rules':
			value = genes[gene_type]
			if random.uniform(0,1) < mutation_probability:
				new_value = random.uniform(value-max_mutation,value+max_mutation)
				if new_value > 1:
					new_value = 1
				elif new_value < 0:
					new_value = 0
				mutated_genes[gene_type] = new_value
			else:
				mutated_genes[gene_type] = value
		else:
			value = genes[gene_type].value
			if random.uniform(0,1) < mutation_probability:
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
	parent_weights = []

	for i in range(numberOfParents):
		fitness = parents[i]['fitness']
		probability_of_parent = fitness//200
		for j in range(probability_of_parent):
			parent_weights.append(i)

	return parent_weights

if __name__ == '__main__':
	main()