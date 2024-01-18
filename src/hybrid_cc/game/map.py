from hybrid_cc.game.cell import Cell


class Map:
    def __init__(self, level):
        self.size = level.size
        self.map = {}
        x, y, z = self.size
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    p = (x, y, z)
                    self.map[p] = Cell(p)
                    there = level.map[p]
                    elems = [there.terrain, there.terrain_mod,
                             there.pickup, there.mob]
                    if there.sides:
                        elems += there.sides
                    for elem in elems:
                        if elem:
                            self.construct_at(p, elem.id, **elem.get_kwargs())

    def get(self, p):
        """Get the cell at location p."""
        return self.map[p]

    def construct_at(self, p, _id, **kwargs):
        """Set the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        return self.map[p].construct(_id, **kwargs)

    def destruct_at(self, p, elem_or_id):
        return self.map[p].destruct(elem_or_id)

    def simple_add(self, p, elem):
        return self.map[p].simple_add(elem)

    def simple_remove(self, p, elem_or_id):
        return self.map[p].simple_remove(elem_or_id)

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.size[0] and
                    0 <= y < self.size[1] and
                    0 <= z < self.size[2])

    def throw_if_oob(self, p):
        if self.is_oob(p):
            raise ValueError(f"Position {p} is out of bounds!")
