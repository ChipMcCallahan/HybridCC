from enum import Enum

from hybrid_cc.shared.layer import Layer


class Id(Enum):
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

    DOOR = (Layer.TERRAIN_MOD, 0)
    THIEF = (Layer.TERRAIN_MOD, 1)
    SOCKET = (Layer.TERRAIN_MOD, 2)
    BUTTON = (Layer.TERRAIN_MOD, 3)
    TOGGLE_WALL = (Layer.TERRAIN_MOD, 4)

    CHIP = (Layer.PICKUP, 0)
    BOMB = (Layer.PICKUP, 1)
    KEY = (Layer.PICKUP, 2)
    TOOL = (Layer.PICKUP, 3)

    PANEL = (Layer.SIDES, 0)
    CORNER = (Layer.SIDES, 1)

    DIRT_BLOCK = (Layer.MOB, 0)
    DIRECTIONAL_BLOCK = (Layer.MOB, 1)
    ICE_BLOCK = (Layer.MOB, 2)
    MONSTER = (Layer.MOB, 3)
    TANK = (Layer.MOB, 4)
    ROBOT = (Layer.MOB, 5)
    PLAYER = (Layer.MOB, 6)

    def layer(self):
        return self.value[0]
