from GroupOfPeople import GroupOfPeople
from utils import mutate_parameter, mutate_quarantine_isolation
from Types import RulesQuarantine, RulesIsolation
from evolutionary_algorithm import run_generations
import const


def main():
	population = []

	for index in range(const.population_size):
		population.append(GroupOfPeople(x=const.x,
										y=const.y,
										healthcare=mutate_parameter(0.5, 0.5),
										hygiene=mutate_parameter(0.5, 0.5),
										mask=mutate_parameter(0.5, 0.5),
										distancing=mutate_parameter(0.5, 0.5),
										curfew=mutate_parameter(0.5, 0.5),
										test_rate=mutate_parameter(0.5, 0.5),
										quarantine_rules=RulesQuarantine(mutate_quarantine_isolation(2, 2)),
										isolation_rules=RulesIsolation(mutate_quarantine_isolation(2, 2))))

	run_generations(initial_population=population)

if __name__ == '__main__':
	main()