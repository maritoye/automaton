from GroupOfPeople import GroupOfPeople
from Types import RulesIsolation, RulesQuarantine
import generate_graphs
import const

X = 100
Y = 100
HEALTHCARE = 0.6
HYGIENE = 0.5
MASK = 0.7
DISTANCING = 0.5
CURFEW = 0.5
TEST_RATE = 0.5
QUARANTINE_RULES = RulesQuarantine.SICK_INFECTIOUS
ISOLATION_RULES = RulesIsolation.SICK_INFECTIOUS


def one_run(x, y, healthcare, hygiene, mask, distancing, curfew, test_rate, quarantine_rules, isolation_rules):
    healthy = []
    infectious = []
    sick = []
    dead = []
    recovered = []

    firstPopulation = GroupOfPeople(x=x, y=y, healthcare=healthcare, hygiene=hygiene, mask=mask, distancing=distancing,
                                    curfew=curfew, test_rate=test_rate, quarantine_rules=quarantine_rules,
                                    isolation_rules=isolation_rules)

    for step in range(251):
        firstPopulation.update()
        stats = firstPopulation.get_brief_statistics()
        healthy.append(stats["healthy"])
        infectious.append(stats["infectious"])
        sick.append(stats["sick"])
        dead.append(stats["dead"])
        recovered.append(stats["recovered"])

        if step == 0 or step % 50 == 0:
            print(step)
            firstPopulation.observe(step)
            print(firstPopulation.get_brief_statistics())
            generate_graphs.graph(healthy, infectious, sick, dead, recovered)

    info = "Parameters: "
    stats = firstPopulation.get_brief_statistics()
    for gene in const.GENE_TYPES:
        info += (gene + ": "+ str(stats[gene]) + ", ")

    generate_graphs.graph(healthy,infectious,sick,dead,recovered)


if __name__ == '__main__':
    one_run(X, Y, HEALTHCARE, HYGIENE, MASK, DISTANCING, CURFEW, TEST_RATE, QUARANTINE_RULES, ISOLATION_RULES)
