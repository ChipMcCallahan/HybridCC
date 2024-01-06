from enum import Enum

from hybrid_cc.shared.layer import Layer


class Id(Enum):
    SPACE = Layer.TERRAIN
    FLOOR = Layer.TERRAIN
    WALL = Layer.TERRAIN
    EXIT = Layer.TERRAIN
    WATER = Layer.TERRAIN
    FIRE = Layer.TERRAIN
    TRICK_WALL = Layer.TERRAIN
    DIRT = Layer.TERRAIN
    ICE = Layer.TERRAIN
    FORCE = Layer.TERRAIN
    TELEPORT = Layer.TERRAIN
    TRAP = Layer.TERRAIN
    GRAVEL = Layer.TERRAIN
    POP_UP_WALL = Layer.TERRAIN
    HINT = Layer.TERRAIN
    CLONER = Layer.TERRAIN

    DOOR = Layer.TERRAIN_MOD
    THIEF = Layer.TERRAIN_MOD
    SOCKET = Layer.TERRAIN_MOD
    TOGGLE_BUTTON = Layer.TERRAIN_MOD
    HOLD_BUTTON = Layer.TERRAIN_MOD
    TOGGLE_WALL = Layer.TERRAIN_MOD

    CHIP = Layer.PICKUP
    BOMB = Layer.PICKUP
    KEY = Layer.PICKUP
    TOOL = Layer.PICKUP

    PANEL = Layer.SIDES
    CORNER = Layer.SIDES

    BLOCK = Layer.MOB
    PLAYER = Layer.MOB
    MONSTER = Layer.MOB
    TANK = Layer.MOB

    def layer(self):
        return self.value
