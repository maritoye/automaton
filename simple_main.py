from GroupOfPeople import GroupOfPeople
from Types import RulesQuarantine, RulesIsolation

x=30
y=30

first = GroupOfPeople(x=x,
						y=y,
						healthcare=0.3,
						hygiene=0.6,
						mask=0.6,
						distancing=0.7,
						curfew=0.7,
						test_rate=0.7,
						quarantine_rules=RulesQuarantine(3),
						isolation_rules=RulesIsolation(4))


for step in range(100):
    first.update()
    if step == 0 or step % 5 == 0:
        print(step)
        first.observe()
        print(first.get_brief_statistics())
        print(first.get_statistics())

