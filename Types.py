from enum import Enum


class PersonState(Enum):
    EMPTY = 0
    HEALTHY = 1
    INFECTIOUS = 2
    SICK = 3
    RECOVERED = 4
    DEATH = 5


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class BackgroundSickness(Enum):
    NO = 0
    YES = 1
    # SLIGHTLY_INCREASED = 1,
    # MODERATE = 2,
    # ABOVE_AVERAGE = 3,
    # HIGH = 4,
    # FATAL = 1


class FollowProtocol(Enum):
    STRICT = 0
    ABOVE_AVERAGE = 1
    MODERATE = 2
    SLIGHTLY = 3
    NO = 4


class Quarantine(Enum):
    NO = 0
    QUARANTINE = 1
    TOTAL_ISOLATION = 2


class AgeGroup(Enum):
    INFANT = range(0, 3)
    CHILD = range(3, 18)
    YOUNG_ADULT = range(18, 30)
    ADULT = range(30, 50)
    MIDDLE_AGE = range(50, 70)
    AGED = range(70, 90)
    OLD = range(90, 110)

class RulesQuarantine(Enum):
    NOONE = 0
    SICK = 1
    SICK_INFECTIOUS = 2
    SICK_INFECTION_NEIGHBORS = 3
    ALL = 4

class RulesIsolation(Enum):
    NOONE = 0
    SICK = 1
    SICK_INFECTIOUS = 2
    SICK_INFECTION_NEIGHBORS = 3
    ALL = 4