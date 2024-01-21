import logging

from hybrid_cc.game.cell import Cell
from hybrid_cc.game.elem_handler import ElemHandler
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id


class Map:
    def __init__(self, level):
        self.elems = ElemHandler()
        self.size = level.size
        self.monster_order = []
        self.map = {}

        seen = set()
        # Find the player and process that location first.
        x, y, z = self.size
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    p = (i, j, k)
                    mob = level.map[p].mob
                    if mob and mob.id == Id.PLAYER:
                        self.parse_there(p, level)
                        seen.add(p)

        # Process all the locations in level.movement next. This ensures
        # intended monster order is maintained.
        for p in level.movement:
            if p not in seen:
                self.parse_there(p, level)
                seen.add(p)

        # Finally process all the other map locations, skipping any we've seen.
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    p = (i, j, k)
                    if p not in seen:
                        self.parse_there(p, level)

    def parse_movement(self, level):
        for p in level.movement:
            if self.map[p].mob:
                self.monster_order.append(self.map[p].mob)
            else:
                logging.warning(f"{level.title}: monster order p {p} did not "
                                f"correspond to a mob.")

    def parse_there(self, p, level):
        there = level.map[p]
        self.map[p] = Cell(p)
        map_elems = [there.terrain, there.terrain_mod,
                     there.pickup, there.mob]
        if there.sides:
            map_elems += there.sides
        for map_elem in map_elems:
            if map_elem:
                elem = self.construct_at(p, map_elem.id,
                                         **map_elem.get_kwargs())
                if isinstance(elem, Mob) and p in level.movement:
                    index = level.movement.index(p)
                    mob_id = elem.mob_id

    def get(self, p):
        """Get the cell at location p."""
        return self.map[p]

    def construct_at(self, p, _id, **kwargs):
        """Set the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        elem = self.elems.construct_at(p, _id, **kwargs)
        self.map[p].add(elem)
        return elem

    def destruct_at(self, p, elem):
        self.map[p].remove(elem)
        self.elems.destruct_at(p, elem)

    def simple_add(self, p, elem):
        return self.map[p].add(elem)

    def simple_remove(self, p, elem_or_id):
        return self.map[p].remove(elem_or_id)

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.size[0] and
                    0 <= y < self.size[1] and
                    0 <= z < self.size[2])

    def throw_if_oob(self, p):
        if self.is_oob(p):
            raise ValueError(f"Position {p} is out of bounds!")
