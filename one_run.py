from GroupOfPeople import GroupOfPeople
from Types import RulesIsolation, RulesQuarantine
import generate_graphs
import const

X = 100
Y = 100
HEALTHCARE = 0.3809509817497183
HYGIENE = 0.9655131652167935
MASK = 1
DISTANCING = 0.7884598250050401
CURFEW = 1
TEST_RATE = 0.9380235823448189
QUARANTINE_RULES = RulesQuarantine.SICK
ISOLATION_RULES = RulesIsolation.SICK
NO_OF_STEPS = 1000


def one_run(x, y, healthcare, hygiene, mask, distancing, curfew, test_rate, quarantine_rules, isolation_rules):
    """
    Runs the model one time with given values
    To be used after the evolutionary model is finished to see the final outcome
    Can also be used alone
    :param x: int size of GroupOfPeople x-direction
    :param y: int size of GroupOfPeople y-direction
    :param healthcare: float the healthcare value float between 0 and 1
    :param hygiene: float the hygiene value float between 0 and 1
    :param mask: float the mask value float between 0 and 1
    :param distancing: float the distancing value float between 0 and 1
    :param curfew: float the curfew value float between 0 and 1
    :param test_rate: float the test_rate value float between 0 and 1
    :param quarantine_rules: enum for what quarantine rules to be set
    :param isolation_rules: enum for what isolation rules to be set
    """
    healthy = []
    infectious = []
    sick = []
    dead = []
    recovered = []

    firstPopulation = GroupOfPeople(x=x, y=y, healthcare=healthcare, hygiene=hygiene, mask=mask, distancing=distancing,
                                    curfew=curfew, test_rate=test_rate, quarantine_rules=quarantine_rules,
                                    isolation_rules=isolation_rules)

    for step in range(NO_OF_STEPS):
        stats = firstPopulation.get_brief_statistics()
        healthy.append(stats["healthy"])
        infectious.append(stats["infectious"])
        sick.append(stats["sick"])
        dead.append(stats["dead"])
        recovered.append(stats["recovered"])

        if step == 0 or step % 25 == 0:
            print(step)
            generate_graphs.graph(healthy, infectious, sick, dead, recovered, str(step))
            firstPopulation.observe(step)
            print(firstPopulation.get_brief_statistics())
        firstPopulation.update()
    info = "Parameters: "
    stats = firstPopulation.get_brief_statistics()
    for gene in const.GENE_TYPES:
        info += (gene + ": "+ str(stats[gene]) + ", ")

    generate_graphs.graph(healthy, infectious, sick, dead, recovered, str(NO_OF_STEPS))


if __name__ == '__main__':
    one_run(X, Y, HEALTHCARE, HYGIENE, MASK, DISTANCING, CURFEW, TEST_RATE, QUARANTINE_RULES, ISOLATION_RULES)
