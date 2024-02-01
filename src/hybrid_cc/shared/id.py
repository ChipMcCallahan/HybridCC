import re
from enum import Enum

from hybrid_cc.shared.layer import Layer


class Id(Enum):
    DEFAULT = (Layer.UNKNOWN, 0)

    SPACE = (Layer.TERRAIN, 0)
    FLOOR = (Layer.TERRAIN, 1)
    WALL = (Layer.TERRAIN, 2)
    EXIT = (Layer.TERRAIN, 3)
    WATER = (Layer.TERRAIN, 4)
    FIRE = (Layer.TERRAIN, 5)
    TRICK_WALL = (Layer.TERRAIN, 6)
    DIRT = (Layer.TERRAIN, 7)
    ICE = (Layer.TERRAIN, 8)
    FORCE = (Layer.TERRAIN, 9)
    TELEPORT = (Layer.TERRAIN, 10)
    TRAP = (Layer.TERRAIN, 11)
    GRAVEL = (Layer.TERRAIN, 12)
    POP_UP_WALL = (Layer.TERRAIN, 13)
    STEPPING_STONE = (Layer.TERRAIN, 14)
    HINT = (Layer.TERRAIN, 15)
    CLONER = (Layer.TERRAIN, 16)
    THIEF = (Layer.TERRAIN, 17)

    DOOR = (Layer.TERRAIN_MOD, 0)
    SOCKET = (Layer.TERRAIN_MOD, 1)
    BUTTON = (Layer.TERRAIN_MOD, 2)
    TOGGLE_WALL = (Layer.TERRAIN_MOD, 3)

    CHIP = (Layer.PICKUP, 0)
    BOMB = (Layer.PICKUP, 1)
    KEY = (Layer.PICKUP, 2)
    FLIPPERS = (Layer.PICKUP, 3)
    FIRE_BOOTS = (Layer.PICKUP, 4)
    SKATES = (Layer.PICKUP, 5)
    SUCTION_BOOTS = (Layer.PICKUP, 6)

    PANEL = (Layer.SIDES, 0)
    CORNER = (Layer.SIDES, 1)

    DIRT_BLOCK = (Layer.MOB, 0)
    ICE_BLOCK = (Layer.MOB, 2)
    MONSTER = (Layer.MOB, 3)
    TANK = (Layer.MOB, 4)
    ROBOT = (Layer.MOB, 5)
    PLAYER = (Layer.MOB, 6)
    PLACEHOLDER = (Layer.MOB, 7)

    def layer(self):
        return self.value[0]

    @staticmethod
    def from_class_name(class_name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return Id[snake_case.upper()]

    @staticmethod
    def id_to_class_name(_id):
        components = _id.name.lower().split('_')
        return ''.join(x.capitalize() for x in components)
