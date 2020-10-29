from GroupOfPeople import GroupOfPeople
from Types import RulesIsolation, RulesQuarantine
import random

firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.5, hygiene=0.5, mask=0.5, distancing=0.6, curfew=0.7,
                                test_rate=0.6, quarantine_rules=RulesQuarantine.SICK_INFECTIOUS,
                                isolation_rules=RulesIsolation.SICK_INFECTIOUS)

# firstPopulation = GroupOfPeople(x=50, y=50, healthcare=0.8, hygiene=0.8, mask=0.8, distancing=0.8, curfew=0.6, test_rate=0.1, quarantine_rules=RulesQuarantine.NOONE, isolation_rules=RulesIsolation.NOONE)

for step in range(100):
    firstPopulation.update()
    if step == 0 or step % 10 == 0:
        print(step)
        firstPopulation.observe()
        print(firstPopulation.get_brief_statistics())
        print(firstPopulation.get_statistics())