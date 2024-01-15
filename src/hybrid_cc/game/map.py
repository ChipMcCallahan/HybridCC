from hybrid_cc.game.elements import instances


class Map:
    def __init__(self, level):
        self.size = level.size
        self.map = {} # p(x, y, z) to cell

    def put(self, p, _id, **kwargs):
        """Set the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")

        snake_case = _id.name.lower()
        camel_case = ''.join([w.capitalize() for w in snake_case])
        class_to_instantiate = getattr(instances, camel_case, None)

        # TODO: make a Cell class
        # self.map[key] = class_to_instantiate(_id, **kwargs)

    def get(self, p):
        """Get the contents of the cell at location p."""
        x, y, z = p
        return self.map[z][y][x]

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.size[0] and
                    0 <= y < self.size[1] and
                    0 <= z < self.size[2])

    def throw_if_oob(self, p):
        if self.is_oob(p):
            raise ValueError(f"Position {p} is out of bounds!")
