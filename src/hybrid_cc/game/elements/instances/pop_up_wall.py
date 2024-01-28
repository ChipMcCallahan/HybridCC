import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import CreateRequest, DestroyRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult


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
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass
    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    @staticmethod
    def test_enter(mob, position, direction):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_exit(self, mob, position, direction):
        if self.count > 1:
            create_request = CreateRequest(eid=self.id,
                                           pos=position, color=self.color,
                                           count=self.count - 1)
        else:
            create_request = CreateRequest(eid=Id.WALL,
                                           pos=position, color=self.color)
        return [
            DestroyRequest(target=self, pos=position),
            create_request
        ]
