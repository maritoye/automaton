from GroupOfPeople import GroupOfPeople
from utils import fitness_function, mutate_parameter
from Types import RulesIsolation, RulesQuarantine

firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.8, hygiene=0.8, mask=0.8, distancing=0.8, curfew=0.6,
                                test_rate=0.1, quarantine_rules=RulesQuarantine.NO_ONE,
                                isolation_rules=RulesIsolation.NO_ONE)

groupsOfPeople = []

for index in range(10):
    groupsOfPeople.append(GroupOfPeople(x=50,
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
        for index in range(10):
            groupsOfPeople[index].update()

    for index in range(10):
        groupsOfPeople[index].get_score()

    groupsOfPeople.sort(key=lambda gop: gop.score, reverse=True)

    for index in range(10):
        print(groupsOfPeople[index].get_brief_statistics())


    # TODO getting the best four! groupsOfPeople[:4]
