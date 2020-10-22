from GroupOfPeople import GroupOfPeople
from utils import fitness_function
from Types import RulesIsolation, RulesQuarantine

firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.6, hygiene=0.6, mask=0.6, distancing=0.6, curfew=0.6, test_rate=0.6, quarantine_rules=RulesQuarantine.SICK_INFECTIOUS_NEIGHBORS, isolation_rules=RulesIsolation.SICK_INFECTIOUS)
for step in range(100):
    firstPopulation.update()
    if step == 0 or step % 10 == 0:
        print(step)
        firstPopulation.observe()
        print(firstPopulation.get_brief_statistics())
        print(firstPopulation.get_statistics())