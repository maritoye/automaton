from Population import Population
from utils import fitness_function
from Types import RulesIsolation, RulesQuarantine

a = Population(x=50, y=50, healthcare=0.6, hygiene=0.6, mask=0.6, distancing=0.6, curfew=0.6, test_rate=0.6, quarantine_rules=RulesQuarantine.SICK_INFECTION_NEIGHBORS, isolation_rules=RulesIsolation.SICK_INFECTIOUS)
for i in range(100):
    a.update()
    if i == 0 or i % 10 == 0:
        print(i)
        a.observe()
        print(a.get_brief_statistics())
        print(a.get_statistics())