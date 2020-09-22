from enum import Enum

class PersonState(Enum):
    EMPTY = 0
    HEALTHY = 1
    INFECTIOUS = 2
    SICK = 3
    RECOVERED = 4
    DEATH = 5
