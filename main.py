from GroupOfPeople import GroupOfPeople
from utils import fitness_function
from Types import RulesIsolation, RulesQuarantine

firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.8, hygiene=0.8, mask=0.8, distancing=0.8, curfew=0.6, test_rate=0.1, quarantine_rules=RulesQuarantine.NOONE, isolation_rules=RulesIsolation.NOONE)
for step in range(100):
    firstPopulation.update()
    if step == 0 or step % 10 == 0:
        print(step)
        firstPopulation.observe()
        print(firstPopulation.get_brief_statistics())
        print(firstPopulation.get_statistics())