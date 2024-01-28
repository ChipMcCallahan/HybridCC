import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR
from hybrid_cc.shared.move_result import MoveResult


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
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass
    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    @staticmethod
    def test_enter(mob, position, direction):
        if mob.id == Id.PLAYER or mob.id == Id.ICE_BLOCK:
            return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_enter(self, mob, position, direction):
        return [
            DestroyRequest(target=self, pos=position),
            CreateRequest(pos=position, eid=Id.FLOOR, color=self.color)
        ]
