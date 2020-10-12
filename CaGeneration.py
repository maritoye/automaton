from Population import Population


class CaGeneration:

    def __init__(self):
        self.population = Population(x=10, y=10, healthcare=0.4, hygiene=0.18, mask=0.21, distancing=0.1, curfew=0.2, test_rate=0.55)


    def run(self):
        pass

    def get_best_parameter_combination(self):
        pass
