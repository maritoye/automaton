from GroupOfPeople import GroupOfPeople
from generate_graphs import plot_fitness_all_generations
from save_data import read_from_json
from utils import mutate_parameter, mutate_quarantine_isolation
from Types import RulesQuarantine, RulesIsolation
from evolutionary_algorithm import run_generations
import const
import time


def main():
	t0 = time.time()
	population = []

	for index in range(const.POPULATION_SIZE):
		population.append(GroupOfPeople(x=const.X,
										y=const.Y,
										healthcare=mutate_parameter(0.5, 0.5),
										hygiene=mutate_parameter(0.5, 0.5),
										mask=mutate_parameter(0.5, 0.5),
										distancing=mutate_parameter(0.5, 0.5),
										curfew=mutate_parameter(0.5, 0.5),
										test_rate=mutate_parameter(0.5, 0.5),
										quarantine_rules=RulesQuarantine(mutate_quarantine_isolation(2, 2)),
										isolation_rules=RulesIsolation(mutate_quarantine_isolation(2, 2))))

	run_generations(initial_population=population)
	dict_data = read_from_json('data.json')
	plot_fitness_all_generations(dict_data)
	t1 = time.time()
	total = t1 - t0
	print(total)


if __name__ == '__main__':
	main()
