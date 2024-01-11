from enum import Enum


class SpaceRule(Enum):
    DEFAULT = 1
    SOLID_BELOW = 2
    MAYBE_SOLID_BELOW = 3
    DEADLY_BELOW = 4
