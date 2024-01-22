import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import WinRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR
from hybrid_cc.shared.move_result import MoveResult


class Exit(Elem):
    kwarg_filter = (COLOR,)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, **kwargs):
        raise NotImplementedError("Implement or remove.")

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    @staticmethod
    def test_enter(mob, position, direction):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_enter(self, mob, position, direction):
        return [
            WinRequest(color=self.color)
        ]
