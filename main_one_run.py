from GroupOfPeople import GroupOfPeople
from Types import RulesIsolation, RulesQuarantine
import generate_graphs
import const

X = 50
Y = 50
HEALTHCARE = 0.5
HYGIENE = 0.5
MASK = 0.5
DISTANCING = 0.6
CURFEW = 0.7
TEST_RATE = 0.55
QUARANTINE_RULES = RulesQuarantine.SICK_INFECTIOUS
ISOLATION_RULES = RulesIsolation.SICK_INFECTIOUS

healthy = []
infectious = []
sick = []
dead = []
recovered = []

firstPopulation = GroupOfPeople(x=X, y=Y, healthcare=HEALTHCARE, hygiene=HYGIENE, mask=MASK, distancing=DISTANCING,
                                curfew=CURFEW, test_rate=TEST_RATE, quarantine_rules=QUARANTINE_RULES,
                                isolation_rules=ISOLATION_RULES)

for step in range(50):
    firstPopulation.update()
    stats = firstPopulation.get_brief_statistics()
    healthy.append(stats["healthy"])
    infectious.append(stats["infectious"])
    sick.append(stats["sick"])
    dead.append(stats["dead"])
    recovered.append(stats["recovered"])

    if step == 0 or step % 10 == 0:
        print(step)
        firstPopulation.observe(step)
        print(firstPopulation.get_brief_statistics())

info = "Parameters: "
stats = firstPopulation.get_brief_statistics()
for gene in const.GENE_TYPES:
    info += (gene + ": "+ str(stats[gene]) + ", ")

generate_graphs.graph(healthy,infectious,sick,dead,recovered)