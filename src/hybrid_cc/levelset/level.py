"""
Module for defining and manipulating game levels in a three-dimensional grid.

This module provides the Level class, which represents a game level in a
three-dimensional space. Each level has a title and a defined size along the
x, y, and z axes. The class supports operations such as querying and setting
the state of cells within the level, checking bounds, and creating levels from
existing CC1 level formats.
"""


class Level:
    """
    Represents a game level in a three-dimensional grid.

    This class models a level as a three-dimensional grid of cells, each of
    which can hold an arbitrary value. The class provides methods for setting
    and querying cell states, checking if a position is within the level's
    bounds, and creating levels from other level formats.
    """
    def __init__(self, x_size=32, y_size=32, z_size=1):
        """
        Initialize a new Level instance.

        :param title: The title of the level.
        :param x_size: The size along the x-axis.
        :param y_size: The size along the y-axis.
        :param z_size: The size along the z-axis.
        """
        self.author = ""
        self.title = title
        self._x_size = x_size
        self._y_size = y_size
        self._z_size = z_size
        self.chips = {}  # map from color enum to count
        self.time = 0
        self.hints = {}  # map from position to string
        self.hint = ""  # default hint if not in dict

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

    def get(self, p, value):
        """Get the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        x, y, z = p
        return self.map[z][y][x]
