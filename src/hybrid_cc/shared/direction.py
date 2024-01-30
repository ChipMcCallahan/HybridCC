from enum import Enum


class Direction(Enum):
    N = (0, -1, 0)
    S = (0, 1, 0)
    E = (1, 0, 0)
    W = (-1, 0, 0)
    UP = (0, 0, 1)
    DOWN = (0, 0, -1)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def _get_direction_string(self):
        return self.name

    @classmethod
    def _from_string(cls, direction_str):
        return cls[direction_str]

    @classmethod
    def from_move(cls, old_p, new_p):
        dx = new_p[0] - old_p[0]
        dy = new_p[1] - old_p[1]
        dz = new_p[2] - old_p[2]
        for direction in cls:
            if direction.value == (dx, dy, dz):
                return direction
        return None

    def is_cardinal(self):
        return self.name in "NESW"

    def right(self):
        if self in [Direction.UP, Direction.DOWN]:
            return self
        direction_str = self._get_direction_string()
        new_direction_str = "NESW"[("NESW".index(direction_str) + 1) % 4]
        return self._from_string(new_direction_str)

    def reverse(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        direction_str = self._get_direction_string()
        new_direction_str = "NESW"[("NESW".index(direction_str) + 2) % 4]
        return self._from_string(new_direction_str)

    def left(self):
        if self in [Direction.UP, Direction.DOWN]:
            return self
        direction_str = self._get_direction_string()
        new_direction_str = "NESW"[("NESW".index(direction_str) + 3) % 4]
        return self._from_string(new_direction_str)
