from Population import Population

a = Population(x=50, y=50, healthcare=0.3, hygiene=0.4, mask=0.3, distancing=0.5, curfew=0.4, test_rate=0.3)
for i in range(100):
    a.update()
    if i == 0 or i % 10 == 0:
        print(i)
        a.observe()