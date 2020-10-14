from Population import Population
from utils import fitness_function

a = Population(x=50, y=50, healthcare=0.1, hygiene=0.1, mask=0.1, distancing=0.1, curfew=0.1, test_rate=0.3)
for i in range(100):
    a.update()
    if i == 0 or i % 10 == 0:
        print(i)
        a.observe()
        print(a.get_brief_statistics())
        print(fitness_function(a.get_brief_statistics()))