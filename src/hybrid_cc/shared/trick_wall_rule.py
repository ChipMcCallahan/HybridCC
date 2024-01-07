from enum import Enum


class TrickWallRule(Enum):
    PERMANENTLY_INVISIBLE = 1
    INVISIBLE_BECOMES_WALL = 2
    BECOMES_FLOOR = 3
    BECOMES_WALL = 4
    PASS_THRU = 5
    SOLID = 6
