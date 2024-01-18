"""Gameboard module."""
from hybrid_cc.game.elements.instances.elem_factory import ElemFactory
from hybrid_cc.game.map import Map


class Gameboard:
    """Gameboard class."""
    def __init__(self, level):
        """Initialize a new Gameboard instance."""
        ElemFactory.initialize()
        self._size = level.size
        self.map = Map(level)
        self.author = ""
        self.title = level.title
        self.chips = {}  # map from color enum to count
        self.time = 0
        self.hints = {}  # map from position to string
        self.hint = ""  # default hint if not in dict
        self.movement = []

    @property
    def size(self):
        """Returns the size of this level's x, y, z dimensions."""
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.size[0] and
                    0 <= y < self.size[1] and
                    0 <= z < self.size[2])

    def get(self, p):
        """Get the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        return self.map.get(p)
