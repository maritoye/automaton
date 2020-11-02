import const


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
			current+=1
		current=0


	new_file.close()

