from GroupOfPeople import GroupOfPeople
from utils import fitness_function, mutate_parameter
from Types import RulesIsolation, RulesQuarantine
from mutation import choose_mutation_direction

firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.8, hygiene=0.8, mask=0.8, distancing=0.8, curfew=0.6,
                                test_rate=0.1, quarantine_rules=RulesQuarantine.NO_ONE,
                                isolation_rules=RulesIsolation.NO_ONE)

groupOfPeoples = []

for index in range(5):
    groupOfPeoples.append(GroupOfPeople(x=50,
                                        y=50,
                                        healthcare=mutate_parameter(0.5, 0.05),
                                        hygiene=mutate_parameter(0.5, 0.05),
                                        mask=mutate_parameter(0.5, 0.05),
                                        distancing=mutate_parameter(0.5, 0.05),
                                        curfew=mutate_parameter(0.5, 0.05),
                                        test_rate=mutate_parameter(0.5, 0.05),
                                        quarantine_rules=RulesQuarantine.NO_ONE,
                                        isolation_rules=RulesIsolation.NO_ONE))

for evolution_index in range(25):
    for step in range(100):
        groupOfPeoples[0].update()
        groupOfPeoples[1].update()
        groupOfPeoples[2].update()
        groupOfPeoples[3].update()
        groupOfPeoples[4].update()
        # firstPopulation.update()
        # if step == 0 or step % 20 == 0:
        #    print(step)
        #    firstPopulation.observe()
        #    print(firstPopulation.get_brief_statistics())
        #    print(firstPopulation.get_statistics())

    bestGroupOfPeoplesIndex = 0
    bestGroupOfPeoplesScore = 0
    for i in range(5):
        if fitness_function(groupOfPeoples[i].get_brief_statistics()) > bestGroupOfPeoplesScore:
            bestGroupOfPeoplesScore = fitness_function(groupOfPeoples[i].get_brief_statistics())
            bestGroupOfPeoplesIndex = i

    # print("Round (",evolution_index, ") ", groupOfPeoples[0].get_brief_statistics())
    # print("Round (",evolution_index, ") ", fitness_function(groupOfPeoples[0].get_brief_statistics()))
    # print("Round (",evolution_index, ") ", groupOfPeoples[1].get_brief_statistics())
    # print("Round (",evolution_index, ") ", fitness_function(groupOfPeoples[1].get_brief_statistics()))
    # print("Round (",evolution_index, ") ", groupOfPeoples[2].get_brief_statistics())
    # print("Round (",evolution_index, ") ", fitness_function(groupOfPeoples[2].get_brief_statistics()))
    # print("Round (",evolution_index, ") ", groupOfPeoples[3].get_brief_statistics())
    # print("Round (",evolution_index, ") ", fitness_function(groupOfPeoples[3].get_brief_statistics()))
    # print("Round (",evolution_index, ") ", groupOfPeoples[4].get_brief_statistics())
    # print("Round (",evolution_index, ") ", fitness_function(groupOfPeoples[4].get_brief_statistics()))

    print(
        "Round %d Winner is %d with score of %d" % (evolution_index, bestGroupOfPeoplesIndex, bestGroupOfPeoplesScore))
    print(groupOfPeoples[bestGroupOfPeoplesIndex].get_brief_statistics())

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'healthcare')
    best_healthcare_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'healthcare')

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'hygiene')
    best_hygiene_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'hygiene')

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'mask')
    best_mask_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'mask')

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'distancing')
    best_distancing_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'distancing')

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'curfew')
    best_curfew_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'curfew')

    # choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'test_rate')
    best_test_rate_score_so_far = choose_mutation_direction(groupOfPeoples[bestGroupOfPeoplesIndex],'test_rate')

    groupOfPeoples = []

    for index in range(5):
        groupOfPeoples.append(GroupOfPeople(x=50,
                                            y=50,
                                            healthcare=mutate_parameter(best_healthcare_score_so_far, 0.01),
                                            hygiene=mutate_parameter(best_hygiene_score_so_far, 0.01),
                                            mask=mutate_parameter(best_mask_score_so_far, 0.01),
                                            distancing=mutate_parameter(best_distancing_score_so_far, 0.01),
                                            curfew=mutate_parameter(best_curfew_score_so_far, 0.01),
                                            test_rate=mutate_parameter(best_test_rate_score_so_far, 0.01),
                                            quarantine_rules=RulesQuarantine.NO_ONE,
                                            isolation_rules=RulesIsolation.NO_ONE))

