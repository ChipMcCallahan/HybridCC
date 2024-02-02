import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult


class Gravel(Elem):
    kwarg_filter = tuple()  # Retain these kwargs only.

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
        if mob.id in (Id.MONSTER, Id.TANK):
            return MoveResult.FAIL, None
        return MoveResult.PASS, None
