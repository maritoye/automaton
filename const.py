POPULATION_SIZE = 12
NUMBER_OF_PARENTS = 4
NUMBER_OF_GENERATIONS = 25
TIME_STEPS_GROUPOFPEOPLE = 100

MUTATION_PROBABILITY = 0.7
MAX_MUTATION = 0.3

X = 25
Y = 25

CHANCE_OF_INITIAL_INFECTION = 0.002

FITNESS_ACCURACY = 200

QUARANTINE_DURATION = 10
ISOLATION_DURATION = 10

GENE_TYPES = {'healthcare', 'hygiene', 'mask', 'distancing', 'curfew', 'test_rate', 'quarantine_rules', 'isolation_rules'}

RUN_DATA = {'POPULATION_SIZE':POPULATION_SIZE, 'NUMBER_OF_PARENTS':NUMBER_OF_PARENTS, 'NUMBER_OF_GENERATIONS':NUMBER_OF_GENERATIONS,
			'TIME_STEPS_GROUPOFPEOPLE':TIME_STEPS_GROUPOFPEOPLE, 'MUTATION_PROBABILITY':MUTATION_PROBABILITY, 'MAX_MUTATION':MAX_MUTATION,
			'X':X, 'Y':Y, 'CHANCE_OF_INITIAL_INFECTION':CHANCE_OF_INITIAL_INFECTION, 'FITNESS_ACCURACY':FITNESS_ACCURACY,
			'QUARANTINE_DURATION':QUARANTINE_DURATION, 'ISOLATION_DURATION':ISOLATION_DURATION}