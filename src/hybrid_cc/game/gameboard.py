"""Gameboard module."""


class Gameboard:
    """Gameboard class."""
    def __init__(self, level):
        """Initialize a new Gameboard instance."""
        self.author = ""
        self.title = ""
        self.size = level
        self.chips = {}  # map from color enum to count
        self.time = 0
        self.hints = {}  # map from position to string
        self.hint = ""  # default hint if not in dict
        self.movement = []

        self.map = [[[None for _ in range(x_size)] for _ in range(y_size)] for _
                    in range(z_size)]

    @property
    def x_size(self):
        """Returns the size of this level's x dimension."""
        return self._x_size

    @property
    def y_size(self):
        """Returns the size of this level's y dimension."""
        return self._y_size

    @property
    def z_size(self):
        """Returns the size of this level's z dimension."""
        return self._z_size

    @property
    def size(self):
        """Returns the size of this level's x, y, z dimensions."""
        return self.x_size, self.y_size, self.z_size

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.x_size and
                    0 <= y < self.y_size and
                    0 <= z < self.z_size)

    def put(self, p, value):
        """Set the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        x, y, z = p
        self.map[z][y][x] = value

    def get(self, p):
        """Get the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        x, y, z = p
        return self.map[z][y][x]
