from enum import Enum


class PersonState(Enum):
    EMPTY = 0
    HEALTHY = 1
    INFECTIOUS = 2
    SICK = 3
    RECOVERED = 4
    DEATH = 5


class Gender(Enum):
    MALE = 0,
    FEMALE = 1


class BackgroundSickness(Enum):
    NO = 0,
    SLIGHTLY_INCREASED = 1,
    MODERATE = 2,
    ABOVE_AVERAGE = 3,
    HIGH = 4,
    FATAL = 5


class FollowProtocol(Enum):
    NO = 0,
    SLIGHTLY = 1,
    MODERATE = 2,
    ABOVE_AVERAGE = 3,
    STRICT = 4


class Quarantine(Enum):
    NO = 0,
    Quarantine = 1,
    TOTAL_ISOLATION = 2,


