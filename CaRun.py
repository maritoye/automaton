from Population import Population


class CaRun:

    def __init__(self, x, y, healthcare, hygiene, mask, distancing, curfew, test_rate):
        self.population = Population(x, y, healthcare, hygiene, mask, distancing, curfew, test_rate)

    def run(self):
        initialize()
        observe()
        while True:
            update()
            observe()
