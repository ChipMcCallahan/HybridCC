import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, SIDES
from hybrid_cc.shared.move_result import MoveResult


class Panel(Elem):
    kwarg_filter = (COLOR, SIDES)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, position, direction):
        if direction.reverse().name in self.sides:
            return MoveResult.FAIL, []
        return MoveResult.PASS, []

    def test_exit(self, mob, position, direction):
        if direction.name in self.sides:
            return MoveResult.FAIL, []
        return MoveResult.PASS, []
