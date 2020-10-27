from GroupOfPeople import GroupOfPeople
from utils import mutate_parameter, RulesQuarantine, RulesIsolation, fitness_function, mutate_parameter_up, \
    mutate_parameter_down


def choose_mutation_direction(selected_group_of_people, name_target_parameter_for_mutation_experiment):
    mutated_group_of_peoples = []
    for index in range(5):
        mutated_group_of_peoples.append(GroupOfPeople(x=50,
                                                      y=50,
                                                      healthcare=mutate_parameter_up(selected_group_of_people.healthcare, 0.05) if name_target_parameter_for_mutation_experiment == 'healthcare' else selected_group_of_people.healthcare,
                                                      hygiene=mutate_parameter_up(selected_group_of_people.hygiene, 0.05) if name_target_parameter_for_mutation_experiment == 'hygiene' else selected_group_of_people.hygiene,
                                                      mask=mutate_parameter_up(selected_group_of_people.mask, 0.05) if name_target_parameter_for_mutation_experiment == 'mask' else selected_group_of_people.mask,
                                                      distancing=mutate_parameter_up(selected_group_of_people.distancing, 0.05) if name_target_parameter_for_mutation_experiment == 'distancing' else selected_group_of_people.distancing,
                                                      curfew=mutate_parameter_up(selected_group_of_people.curfew, 0.05) if name_target_parameter_for_mutation_experiment == 'curfew' else selected_group_of_people.curfew,
                                                      test_rate=mutate_parameter_up(selected_group_of_people.test_rate, 0.05) if name_target_parameter_for_mutation_experiment == 'test_rate' else selected_group_of_people.test_rate,
                                                      quarantine_rules=RulesQuarantine.NO_ONE,
                                                      isolation_rules=RulesIsolation.NO_ONE))

    for index in range(5):
        mutated_group_of_peoples.append(GroupOfPeople(x=50,
                                                      y=50,
                                                      healthcare=mutate_parameter_down(selected_group_of_people.healthcare, 0.05) if name_target_parameter_for_mutation_experiment == 'healthcare' else selected_group_of_people.healthcare,
                                                      hygiene=mutate_parameter_down(selected_group_of_people.hygiene, 0.05) if name_target_parameter_for_mutation_experiment == 'hygiene' else selected_group_of_people.hygiene,
                                                      mask=mutate_parameter_down(selected_group_of_people.mask, 0.05) if name_target_parameter_for_mutation_experiment == 'mask' else selected_group_of_people.mask,
                                                      distancing=mutate_parameter_down(selected_group_of_people.distancing, 0.05) if name_target_parameter_for_mutation_experiment == 'distancing' else selected_group_of_people.distancing,
                                                      curfew=mutate_parameter_down(selected_group_of_people.curfew, 0.05) if name_target_parameter_for_mutation_experiment == 'curfew' else selected_group_of_people.curfew,
                                                      test_rate=mutate_parameter_down(selected_group_of_people.test_rate, 0.05) if name_target_parameter_for_mutation_experiment == 'test_rate' else selected_group_of_people.test_rate,
                                                      quarantine_rules=RulesQuarantine.NO_ONE,
                                                      isolation_rules=RulesIsolation.NO_ONE))

    for step in range(100):
        for index in range(10):
            mutated_group_of_peoples[index].update()

    best_mutated_index = 0
    best_mutated_score = 0
    for i in range(10):
        if fitness_function(mutated_group_of_peoples[i].get_brief_statistics()) > best_mutated_score:
            best_mutated_score = fitness_function(mutated_group_of_peoples[i].get_brief_statistics())
            best_mutated_index = i

    print(mutated_group_of_peoples[best_mutated_index].get_brief_statistics())
    print(selected_group_of_people.get_brief_statistics()[name_target_parameter_for_mutation_experiment])
    print(mutated_group_of_peoples[best_mutated_index].get_brief_statistics()[name_target_parameter_for_mutation_experiment])
    return selected_group_of_people.get_brief_statistics()[name_target_parameter_for_mutation_experiment] + 0.05 if mutated_group_of_peoples[best_mutated_index].get_brief_statistics()[name_target_parameter_for_mutation_experiment] > (selected_group_of_people.get_brief_statistics()[name_target_parameter_for_mutation_experiment]) else mutated_group_of_peoples[best_mutated_index].get_brief_statistics()[name_target_parameter_for_mutation_experiment]
    # return mutated_group_of_peoples[best_mutated_index].get_brief_statistics()