import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared.kwargs import COLOR
from hybrid_cc.shared.move_result import MoveResult


class Wall(Elem):
    kwarg_filter = (COLOR,)  # Retain these kwargs only.

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
    @staticmethod
    def test_enter(mob, p, d):
        return MoveResult.FAIL, None
