from GroupOfPeople import GroupOfPeople


class CaRun:

    def __init__(self, x, y, healthcare, hygiene, mask, distancing, curfew, test_rate):
        self.population = GroupOfPeople(x, y, healthcare, hygiene, mask, distancing, curfew, test_rate)

    def run(self):
        initialize()
        observe()
        while True:
            update()
            observe()