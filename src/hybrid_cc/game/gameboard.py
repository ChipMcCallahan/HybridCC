"""Gameboard module."""
from enum import Enum

from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.map import Map
from hybrid_cc.game.move_handler import MoveHandler
from hybrid_cc.shared.move_result import MoveResult


class Gameboard:
    """Gameboard class."""

    class State(Enum):
        PLAY = 1
        WIN = 2
        LOSE = 3

    def __init__(self, level):
        """Initialize a new Gameboard instance."""
        self._size = level.size
        self.map = Map(level)
        self.elems = self.map.elems
        self.move_handler = MoveHandler(self.map)
        self.author = ""
        self.title = level.title
        self.chips = {}  # map from color enum to count
        self.time = level.time
        self.hints = {}  # map from position to string
        self.hint = ""  # default hint if not in dict
        self.tick = 0
        self.state = Gameboard.State.PLAY

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

    def viewport_center(self, viewport_size=9):
        margin = viewport_size // 2
        x, y, z = Player.position or (0, 0, 0)
        x, y = max(x, margin), max(y, margin)
        x = min(x, self.size[0] - margin - 1)
        y = min(y, self.size[1] - margin - 1)
        return x, y, z

    def do_logic(self, inputs):
        raw_moves = self.elems.collect_move_plans(inputs, self.tick)

        moved = set()
        for move in raw_moves:
            mob_id, dirs = move
            mob = self.elems.get_mob(mob_id)
            if not mob or mob_id in moved:
                continue
            for d in dirs:
                result = self.move_handler.move(mob, d, self.tick)
                if result == MoveResult.PASS:
                    moved.add(mob.mob_id)
                    break
        self.tick += 1
        if self.time > 0 and self.time_remaining() == 0:
            self.transition(Gameboard.State.LOSE)

    def transition(self, state):
        if self.state == Gameboard.State.PLAY:
            self.state = state

    def time_remaining(self):
        return max(self.time - self.tick // 10, 0)
