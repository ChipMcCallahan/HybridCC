import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import ENTERS_DIRT


class Dirt(Elem):
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
    def test_enter(mob, p, direction):
        if mob.tagged(ENTERS_DIRT):
            return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_enter(self, mob, p, direction):
        return [
            DestroyRequest(target=self, p=p),
            CreateRequest(p=p, id=Id.FLOOR, color=self.color)
        ]
