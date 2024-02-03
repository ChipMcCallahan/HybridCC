import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import CreateRequest, DestroyRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import ENTERS_DIRT


class PopUpWall(Elem):
    kwarg_filter = (COLOR, COUNT)  # Retain these kwargs only.

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
        if mob.tagged(ENTERS_DIRT):
            return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_exit(self, mob, p, d):
        if self.count > 1:
            create_request = CreateRequest(id=self.id,
                                           p=p, color=self.color,
                                           count=self.count - 1)
        else:
            create_request = CreateRequest(id=Id.WALL,
                                           p=p, color=self.color)
        return [
            DestroyRequest(src=mob, tgt=self, p=p),
            create_request
        ]
