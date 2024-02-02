import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared import Direction
from hybrid_cc.shared.kwargs import COLOR, SIDES
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import PUSHABLE


class Corner(Elem):
    kwarg_filter = (COLOR, SIDES)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------


    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, p, direction):
        if direction.reverse().name in self.sides:
            return MoveResult.FAIL, []
        return MoveResult.PASS, []

    def test_exit(self, mob, p, direction):
        if direction.name not in self.sides:
            return MoveResult.PASS, []

        # This prevents unintuitive behavior with ants, paramecia, and teeth,
        # while still allowing ice moves to work as intended.
        if not mob.tagged(PUSHABLE) and direction != mob.direction:
            return MoveResult.FAIL, []

        sides = set(Direction[d] for d in self.sides)
        sides.remove(direction)
        orthogonal = sides.pop().reverse()
        return MoveResult.FAIL, [MoveRequest(mob_id=mob.mob_id,
                                             direction=orthogonal)]
