"""Gameboard module."""
from hybrid_cc.game.map import Map


class Gameboard:
    """Gameboard class."""
    def __init__(self, level):
        """Initialize a new Gameboard instance."""
        self.map = Map(level)
        self.author = ""
        self.title = ""
        self.chips = {}  # map from color enum to count
        self.time = 0
        self.hints = {}  # map from position to string
        self.hint = ""  # default hint if not in dict
        self.movement = []
